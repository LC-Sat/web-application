# =============================================================================
# Imports
# =============================================================================


import matplotlib.pyplot as plt
import numpy as np
import json
import os


# =============================================================================
# Scripts
# =============================================================================


class Chart:


	def __init__(self, debug, config_path, static_path, language):

		self.debug = debug
		self.language = language
		self.static_path = static_path

		with open(config_path, "r", encoding = "utf-8") as file:

			self.config = json.load(file)
			file.close()

		return


	def __str__(self):

		return "Chart class"


	def reload(self, debug, config_path):

		self.debug = debug

		with open(config_path, "r", encoding = "utf-8") as file:

			self.config = json.load(file)
			file.close()

		return


	def draw_chart(self, x_data, y_data, title, x_label, y_label, line_width):

		# Creating title if no title given
		chart_title = title

		if chart_title == "":

			v = []

			for n, data in enumerate(y_data):

				v.append(self.language.get_text(data["prefix"]))
				v.append(', ')
				
				if n % 3 == 0:

					v.append("\n") 

			chart_title = ''.join(v) + "\n" + self.language.get_text("dependingOn") + " " + self.language.get_text(x_data[0]["prefix"]) + "."


		# creating chart y_label if user didn't provide one
		chart_ylabel = y_label
		if chart_ylabel == "":

			for data in y_data:

				chart_ylabel += self.language.get_text(data["prefix"]) + " (" + self.language.get_text("in") + " " + str(data["unit"]) + ")\n" 


		# # creating chart x_label if user didn't provide one
		chart_xlabel = x_label
		if chart_xlabel == "":

			chart_xlabel += self.language.get_text(x_data[0]["prefix"]) + " (" + self.language.get_text("in") + " " + str(x_data[0]["unit"]) + ")"


		if x_data[0]["name"] != "time":

			X = np.array(x_data[0]["values"], dtype="float64")

		else:

			X = []
			i = 0
			n = 0

			while n < len(y_data[0]["values"]):

				X.append(i)
				n += 1
				i += 1 * self.config["recordingFrequency"]


		fig, axs = plt.subplots(len(y_data), sharex = True)
		fig.set_size_inches(8, 20)


		for r, data in enumerate(y_data):
			
			y = []

			for i in range(0, len(X) -1, 1):

				try:

					y.append(data["values"][i])

				except Exception:

					y.append(0)
			

			Y = np.array(data["values"], dtype="float64")

			axs[r].plot(X, Y, str(data["color"]), marker = data["point"], linestyle = data["line"], linewidth = line_width)

			
			axs[r].set(xlabel=chart_xlabel, ylabel=self.language.get_text(data["prefix"]) + " (" + self.language.get_text("in") + " " + str(data["unit"]) + ')')

			# place on both sides values
			if r % 2 != 0:

				axs[r].tick_params(axis='y', which='both', labelleft=False, labelright=True)

			else:

				axs[r].tick_params(axis='y', which='both', labelleft=True, labelright=False)


		if self.debug:

			print("------------------[CHARTS]------------------")
			print(f"Chart title | {chart_title}")
			print(f"Chart x_label | {chart_xlabel}")
			print(f"Chart y_label | {chart_ylabel}")
			print(f"X values | {x_data}")
			print(f"Y values | {y_data}")
			print(f"Line width | {line_width}")
			print("----------------[END CHARTS]----------------\n")


		plt.legend()
		fig.suptitle(chart_title)
		plt.savefig(os.path.join(self.static_path, "chart.png"), dpi=100)

		return