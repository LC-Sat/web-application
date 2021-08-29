# =============================================================================
# Imports
# =============================================================================


import requests
import json
import time
from datetime import date
from datetime import datetime
import os
import zipfile
import shutil
import io


# =============================================================================
# Scripts
# =============================================================================


class Api:


	def __init__(self, debug, url_base, urls_path, log_path, data_path):

		self.debug = debug
		self.url_base = url_base
		self.log_path = log_path
		self.data_path = data_path

		# Load urls from urls.json file

		with open(urls_path + "/urls.json", 'r') as file:

			self.urls = json.load(file)
			file.close()


	def __str__(self):

		return "Api class"


	def send_request(self, url):

		# Send request and return content

		r = requests.get(self.url_base + url)

		return r


	def get_cansat_status(self):

		# Request for Cansat Status

		r = self.send_request(self.urls["status"])
		if r == "":
			print("api error")
			return ""

		print(r.content)
		status = str(r.content).replace("b'", "").replace("\\n'", "")
		return json.loads(status)


	def activate(self, url, element):

		# Send request then check if element has been unactivated

		r = self.send_request(url)

		# Return "" if something went wrong

		if r == "":

			return ""

		else:

			time.sleep(1)
			status = self.get_cansat_status()

			if status == "":

				return ""

			else:

				# Return True if element is unactivated
				# Return False if element is not unactivated

				if status[element] == "True" :

					return True

				else:

					return False


	def unactivate(self, url, element):

		# Send request then check if element has been unactivated

		r = self.send_request(url)

		# Return "" if something went wrong

		if r == "":

			return ""

		else:

			time.sleep(1)
			status = self.get_cansat_status()

			if status == "":

				return ""

			else:

				# Return True if element is unactivated
				# Return False if element is not unactivated

				if status[element] == False:

					return True

				else:

					return False


	def start_recording(self):

		# Send request to stop recording data
		# Wait 1s and check if the recording has stopped

		r = self.activate(self.urls["start_recording"], "capturing")

		if self.debug:

			print("-----------------[API]------------------")
			print(f"Activating record | recording status: [{r}]")
			print("----------------[END API]---------------\n")


		if r:

			return True

		elif r == "":

			return ""

		else:

			return False


	def stop_recording(self):

		# Send request to start recording data
		# Wait 1s and check if the recording has started

		r = self.unactivate(self.urls["stop_recording"], "capturing")

		if self.debug:

			print("-----------------[API]------------------")
			print(f"Stopping record | recording status: [{r}]")
			print("----------------[END API]---------------\n")


		if r:

			return True

		elif r == "":

			return ""

		else:

			return False


	def enable_encryption(self):

		# Send request to enable encryption option
		# Wait 1s and check if the encryption option is enabled

		r = self.activate(self.urls["start_encryption"], "encryption")

		if self.debug:

			print("-----------------[API]------------------")
			print(f"Enable encryption | encryption status: [{r}]")
			print("----------------[END API]---------------\n")

		if r:

			return True

		elif r == "":

			return ""

		else:

			return False


	def disable_encryption(self):

		# Send request to disable encryption option
		# Wait 1s and check if the encryption option is disabled

		r = self.unactivate(self.urls["stop_encryption"], "encryption")

		if self.debug:

			print("-----------------[API]------------------")
			print(f"Disable encryption | encryption status: [{r}]")
			print("----------------[END API]---------------\n")

		if r:

			return True

		elif r == "":

			return ""

		else:

			return False


	def start_buzzer(self):

		# Send request to start Buzzer
		# Wait 1s and check if buzzer has started

		r = self.activate(self.urls["start_buzzer"], "buzzer")

		if self.debug:

			print("-----------------[API]------------------")
			print(f"Start buzzer | buzzer status: [{r}]")
			print("----------------[END API]---------------\n")

		if r:

			return True

		elif r == "":

			return ""

		else:

			return False


	def stop_buzzer(self):

		# Send request to stop Buzzer
		# Wait 1s and check if buzzer has stopped

		r = self.unactivate(self.urls["stop_buzzer"], "buzzer")

		if self.debug:

			print("-----------------[API]------------------")
			print(f"Start buzzer | buzzer status: [{r}]")
			print("----------------[END API]---------------\n")

		if r:

			return True

		elif r == "":

			return ""

		else:

			return False


	def shutdown_cansat(self):

		# Send request to stop CanSat
		# Wait 2s and check if shutdown process has started

		r = self.send_request(self.urls["shutdown"])

		if self.debug:

			print("-----------------[API]------------------")
			print(f"Start buzzer | buzzer status: [{r}]")
			print("----------------[END API]---------------\n")

		if r == "":

			return ""

		time.sleep(2)

		if self.send_request(self.urls["shutdown_status"])["shutdown"]:

			return True

		else:

			return False


	def get_logs(self):

		# Request for logs and stored them if a log file called %data.txt
		# 	- if no file then create it
		# 	- else append content to current file

		r = self.send_request(self.urls["logs"])
		log_name = str(date.today().strftime("%b-%d-%Y")+".txt")

		if self.debug:

			print("-----------------[API]------------------")
			print(f"Getting logs | log status: [{r}]")
			print(f"Log name | {log_name}")
			print("----------------[END API]---------------\n")

		with open(os.path.join(self.log_path, log_name), 'ab') as l:

			l.write(r.content)
			l.close()


	def get_sub_folders(self, path):

		# Search for subfolers:
		# 	- if there is a subfolder then add its name to path
		# 	- if none then stop

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

		if self.debug:

			print("-----------------[API]------------------")
			print(f"Get data | buzzer status: [{r}]")

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

		if self.debug:

			print(f"Getting unzipped data | path: [{directory}]")

		if os.listdir(os.path.dirname(directory))[0].endswith(".aes"):
			
			try:

				dirname = str(int(os.listdir(os.path.join(self.data_path, "encrypted"))[-1]) + 1)

			except Exception:

				dirname = "0"

			os.mkdir(self.data_path + "/encrypted/" + dirname)
			shutil.move(self.data_path + "data.tar.gz", self.data_path + "/encrypted/" + dirname)

			if self.debug:

				print(f"Moving files | path: [{str(self.data_path + 'data.tar.gz', self.data_path + '/encrypted/' + dirname)}]")
				print("----------------[END API]---------------\n")

			for file in os.listdir(os.path.join(self.data_path, "data")):
				shutil.move(os.path.join(os.path.join(self.data_path, "data"), file), self.data_path + "/encrypted/" + dirname)

		else:

			try:

				dirname = str(int(os.listdir(os.path.join(self.data_path, "normal"))[-1]) + 1)

			except Exception:

				dirname = "0"

			os.mkdir(self.data_path + "/normal/" + dirname)
			shutil.move(self.data_path + "data.tar.gz", self.data_path + "/normal/" + dirname)

			if self.debug:

				print(f"Moving files | path: [{str(self.data_path + 'data.tar.gz', self.data_path + '/normal/' + dirname)}]")
				print("----------------[END API]---------------\n")


			for file in os.listdir(os.path.join(self.data_path, "data")):

				shutil.move(file, self.data_path + "/normal/" + dirname)

		return True
		
