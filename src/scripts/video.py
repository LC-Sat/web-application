# =============================================================================
# Imports
# =============================================================================


import cv2 as cv
from cv2 import VideoWriter, VideoWriter_fourcc
import numpy as np
import json
import pickle
import os
import shutil
import math


# =============================================================================
# Scripts
# =============================================================================


class Video:


	def __init__(self, debug, static_path, config_path):

		self.debug = debug
		self.static_path = static_path

		with open(os.path.join(config_path, "video.json"), 'r', encoding = "utf-8") as f:

			self.config = json.load(f)
			f.close()

		return


	def __str__(self):

		return "Video class"


	def reload(self, debug, config_path):

		self.debug = debug

		with open(os.path.join(config_path, "video.json"), 'r', encoding = "utf-8") as f:

			self.config = json.load(f)
			f.close()

		return


	def render_classic_video(self, data_path):

		# Load video (cam.mp4) to static/result folder
		with open(os.path.join(data_path, "cam.mp4"), 'rb') as file:

			with open(os.path.join(self.static_path, "result/cam.mp4"), 'wb') as f:

				f.write(file.read())
				f.close()

			file.close()

			if self.debug:

				print("------------------[VIDEO]------------------")
				print(f"Load video")
				print("----------------[END VIDEO]----------------\n")

		return


	def create_new_row_pixels(self, increment_coefficient, increase_size_factor, starting_value):

		# Create a smooth gradient from starting value to next value

		array = []

		current_value = starting_value

		for i in range(0, increase_size_factor):

			array.append(increment_coefficient)
			current_value += increment_coefficient

		if self.debug:

				print("------------------[VIDEO]------------------")
				print(f"Create new pixels | {array}")
				print("----------------[END VIDEO]----------------\n")

		return array[::-1]


	def convert_to_rgb(self, value):

		medium_temperature = (self.config["minimalTemperature"] + self.config["maximalTemperature"]) / 2
		medium_length = ((math.sqrt(self.config["minimalTemperature"] ** 2)) + (math.sqrt(self.config["maximalTemperature"] ** 2))) / 2

		increase_color_factor = 255 / medium_length
		decrease_color_factor = -255 / medium_length

		# Color from blue to green
		if value < medium_temperature:

			factor = medium_length - (math.sqrt(value ** 2))
			color = []

			color.append(0)
			color.append(0 + (increase_color_factor * factor))
			color.append(255 - (decrease_color_factor * factor))

			if self.debug:

				print("------------------[VIDEO]------------------")
				print(f"Create color | {color}")
				print("----------------[END VIDEO]----------------\n")
			
			return color

		# Color from green to red
		elif value > medium_temperature:

			factor = medium_length - (math.sqrt(value ** 2))
			color = []
			
			color.append(0 + (increase_color_factor * factor))
			color.append(255 - (decrease_color_factor * factor))
			color.append(0)

			if self.debug:

				print("------------------[VIDEO]------------------")
				print(f"Create color | {color}")
				print("----------------[END VIDEO]----------------\n")

			return color 

		else:

			return self.config["mediumColor"]


	def render_thermal_video(self, data_path):

		thermal_cam_data = pickle.load(open(os.path.join(data_path, "data.bin"), "rb"))["therm"]

		# calculate the number of pixels to append between each original pixels
		increase_size_factor = self.config["videoSize"] / 8
		increase_size_factor = increase_size_factor * 7 + 8
		increase_size_factor = int((self.config["videoSize"] / 8) + (((self.config["videoSize"] - increase_size_factor) - 2) / 7))
		

		#adding new pixels

		for frame in thermal_cam_data:

			for row	in frame:

				new_pixels_arrays = []

				for p in range(0, 7, 1):

					# create proportionality coefficient
					increment_coefficient = (row[p + 1] - row[p]) / increase_size_factor
					new_pixels_arrays.append(self.create_new_row_pixels(increment_coefficient, increase_size_factor, row[p]))

				# adding new pixels
				
				new_pixels_arrays.reverse()
				
				for i in range(len(new_pixels_arrays) - 1,  0, -1):

					for p in new_pixels_arrays[i]:

						np.insert(row, i + 1, p)


			# adding the right and left edges
			for row in frame:

				np.insert(row, 0, row[0])
				np.append(row, row[-1])

			# adding the bottom and top edges
			np.insert(frame, 0, frame[0])
			np.append(frame, frame[-1])

		# writing the video

		fourcc = VideoWriter_fourcc(*'MP42')
		video = VideoWriter(os.path.join(self.static_path, "result/thermal.avi"), fourcc, float(self.config["FPS"]), (self.config["videoSize"], self.config["videoSize"]))

		# convert pixel to color and create frame
		for frame in thermal_cam_data:

			colored_frame = []

			for row in frame:

				colored_row = []

				for pixel in row:

					colored_row.append(self.convert_to_rgb(pixel))

				colored_frame.append(colored_row)

			image = np.uint8(colored_frame)

			video.write(image)

		video.release()

		if self.debug:

			print("------------------[VIDEO]------------------")
			print(f"Video created")
			print("----------------[END VIDEO]----------------\n")


		return