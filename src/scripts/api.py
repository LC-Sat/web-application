# =============================================================================
# Imports
# =============================================================================


import requests
import json
import time
from datetime import date
import os
import zipfile
import shutil
import io


# =============================================================================
# Scripts
# =============================================================================


class Api:


	def __init__(self, url_base, urls_path, log_path, data_path):

		self.url_base = url_base
		self.log_path = log_path
		self.data_path = data_path

		with open(urls_path + "/urls.json", 'r') as file:

			self.urls = json.load(file)
			file.close()


	def __str__(self):

		return "Api class"


	def send_request(self, url):

		r = requests.get(self.url_base + url)

		return r


	def get_cansat_status(self):

		r = self.send_request(self.urls["status"])

		if r == "":

			return ""

		status = str(r.content).replace("b'", "").replace("\\n'", "")
		return json.loads(status)


	def activate(self, url, element):

		r = self.send_request(url)

		if r == "":

			return ""

		else:

			time.sleep(1)
			status = self.get_cansat_status()

			if status == "":

				return ""

			else:

				if status[element] == "True" :

					return True

				else:

					return False


	def unactivate(self, url, element):

		r = self.send_request(url)

		if r == "":

			return ""

		else:

			time.sleep(1)
			status = self.get_cansat_status()

			if status == "":

				return ""

			else:

				if status[element] == False:

					return True

				else:

					return False


	def start_recording(self):

		r = self.activate(self.urls["start_recording"], "capturing")

		if r:

			return True

		elif r == "":

			return ""

		else:

			return False


	def stop_recording(self):

		r = self.unactivate(self.urls["stop_recording"], "capturing")

		if r:

			return True

		elif r == "":

			return ""

		else:

			return False


	def enable_encryption(self):

		r = self.activate(self.urls["start_encryption"], "encryption")

		if r:

			return True

		elif r == "":

			return ""

		else:

			return False


	def disable_encryption(self):

		r = self.unactivate(self.urls["stop_encryption"], "encryption")

		if r:

			return True

		elif r == "":

			return ""

		else:

			return False


	def start_buzzer(self):

		r = self.activate(self.urls["start_buzzer"], "buzzer")

		if r:

			return True

		elif r == "":

			return ""

		else:

			return False


	def stop_buzzer(self):

		r = self.unactivate(self.urls["stop_buzzer"], "buzzer")

		if r:

			return True

		elif r == "":

			return ""

		else:

			return False


	def shutdown_cansat(self):

		r = self.send_request(self.urls["shutdown"])

		if r == "":

			return ""

		time.sleep(2)

		if self.send_request(self.urls["shutdown_status"])["shutdown"]:

			return True

		else:

			return False


	def get_logs(self):

		r = self.send_request(self.urls["logs"])
		log_name = str(date.today().strftime("%b-%d-%Y")+".txt")

		with open(os.path.join(self.log_path, log_name), 'ab') as l:

			l.write(r.content)
			l.close()


	def get_sub_folders(self, path):

		try:
			if os.listdir(path)[0].endswith(""):
				
				return os.listdir(path)[0]

			else:
				return ""

		except Exception:

			return ""

	def get_recorded_data(self):
		
		# Get the file content

		try:

			r = requests.get(self.url_base + "/api/download")

		except Exception:

			return False

		# Create a data.tar.gz file at data/
		# Unpack the compressed file creating a data/data folder

		with open(self.data_path + "data.tar.gz", "wb") as f:

			f.write(r.content)
			f.close()

		shutil.unpack_archive(self.data_path + "data.tar.gz", self.data_path)

		directory = os.path.join(self.data_path, "data")

		# If data/data folder contains subfolders:
		# 	- look in each subfolders until it finds the files

		while True:

			if self.get_sub_folders(directory) == "":

				break

			else:

				directory = os.path.join(directory, self.get_sub_folders(directory))

		# Get the file extensions:
		# 	- if .aes then move files to data/encrypted/id
		# 	- else move files to data/normal/id
		print(directory)

		if os.listdir(os.path.dirname(directory))[0].endswith(".aes"):
			
			try:

				dirname = str(int(os.listdir(os.path.join(self.data_path, "encrypted"))[-1]) + 1)

			except Exception:

				dirname = "0"

			os.mkdir(self.data_path + "/encrypted/" + dirname)
			shutil.move(self.data_path + "data.tar.gz", self.data_path + "/encrypted/" + dirname)

			for file in os.listdir(os.path.join(self.data_path, "data")):
				print(file)
				print(self.data_path + "/encrypted/" + dirname)
				print(dirname)
				shutil.move(os.path.join(os.path.join(self.data_path, "data"), file), self.data_path + "/encrypted/" + dirname)

		else:

			try:

				dirname = str(int(os.listdir(os.path.join(self.data_path, "normal"))[-1]) + 1)

			except Exception:

				dirname = "0"

			os.mkdir(self.data_path + "/normal/" + dirname)
			shutil.move(self.data_path + "data.tar.gz", self.data_path + "/normal/" + dirname)

			for file in os.listdir(os.path.join(self.data_path, "data")):

				shutil.move(file, self.data_path + "/normal/" + dirname)

		return True
		
