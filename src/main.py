# =============================================================================
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Thomas HODSON
# Created Date: August 2021
# =============================================================================
# This program was created for the Lc sat team, qualified for the international phase of the CanSat competition.
# This program processed the data recorded during the ascent, drop and descent of the CanSat.
# This program also communicates with the CanSat's computer to send the user's commands. 
# =============================================================================


# =============================================================================
# Imports
# =============================================================================

# Import native librairies:

import os
import sys
import subprocess
from datetime import date
from datetime import datetime
import numpy
import json
import zipfile
import shutil
import time
import io
import pickle


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Runs pip install -r requirements.txt
# 	- if importation error:
# 		- log errors
# 		- terminate script

def log(text):

	log_path = os.path.join(BASE_DIR, "logs/webapp")
	log_name = str(date.today().strftime("%b-%d-%Y")+".txt")

	with open(os.path.join(log_path, log_name), "a") as log:

		log.write('\n' + str(text) + '\n')

		log.close()


def install_packages():

	try:
		file_path = os.path.join(BASE_DIR, "requirements.txt")
		subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", file_path])

	except Exception as e:

		log(e)

		sys.exit()


#  If importing external librairies fails then call install_packages 

try:
	import yaml
	from flask import Flask, render_template, redirect, url_for, request
	import matplotlib.pyplot as plt
	import cv2 as cv
	import folium
	import requests

except Exception as e:
	install_packages()

finally:

	try:
		import yaml
		from flask import Flask, render_template, redirect, url_for, request
		import matplotlib.pyplot as plt
		import cv2 as cv
		import folium
		import requests

	except Exception as e:

		log_path = os.path.join(BASE_DIR, "logs")
		log_name = str(date.today().strftime("%b-%d-%Y")+".txt")

		log(e)

		sys.exit()


# =============================================================================
# Local imports
# =============================================================================


try:
	from scripts.api import Api
	from scripts.graphs import Chart
	from scripts.maps import Map
	from scripts.video import Video

except Exception as e:

	log(e)
	sys.exit()


# =============================================================================
# Consts
# =============================================================================


SETTINGS_PATH = os.path.join(BASE_DIR, 'res/settings/')
TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'res/templates/')
LANGUAGE_FOLDER = os.path.join(BASE_DIR, 'res/i18n/')
LOG_PATH = os.path.join(BASE_DIR, 'logs/')
DATA_PATH = os.path.join(BASE_DIR, 'data/')
STATIC_PATH = os.path.join(BASE_DIR, 'src/static/')
THEME_PATH = os.path.join(BASE_DIR, 'res/theme/')
APP = Flask(__name__)
USER_LOGIN = False

# =============================================================================
# Controllers class
# =============================================================================


# Settings class

class Settings:


	def __init__(self, file_path):

		self.debug = False

		with open(file_path, 'r') as file:

			self.settings_data = yaml.load(file)

			file.close()


	def __str__(self):

		return "Settings class"

	
	def get_settings_value(self, value):

		if self.debug:

			print("-----------------[SETTINGS]-----------------")
			print(f"Settings | {str(self.settings_data[value])}")
			print("---------------[END SETTINGS]---------------\n")
		
		return str(self.settings_data[value])


# Language class

class Language:


	def __init__(self, debug, file_path):

		self.debug = debug

		with open(file_path, 'r') as file:

			self.language_data = json.load(file)

			file.close()


	def __str__(self):

		return "Language class"


	def get_text(self, text):

		if self.debug:

			print("-----------------[LANGUAGE]-----------------")
			print(f"Language | {str(self.language_data[text])}")
			print("---------------[END LANGUAGE]---------------\n")

		return self.language_data[text]


# =============================================================================
# Instantiate classes
# =============================================================================


_settings = Settings(
	os.path.join(SETTINGS_PATH, 'settings.yaml')
	)

DEBUG = _settings.debug = _settings.get_settings_value("debug")
_settings.debug = DEBUG

_language = Language(
	DEBUG,
	LANGUAGE_FOLDER + _settings.get_settings_value("language") + ".json"
	)

_api = Api(
	DEBUG,
	_settings.get_settings_value("cansatIp"),
	SETTINGS_PATH,
	os.path.join(LOG_PATH, "cansat/"),
	DATA_PATH
	)

if _settings.get_settings_value("debug"):

	print("------------------[DEBUG]------------------")
	print(f"DEBUG | {_settings}\t OK")
	print(f"DEBUG | {_language}\t OK")
	print(f"DEBUG | {_api}\t      OK")
	print("----------------[END DEBUG]----------------\n")


# =============================================================================
# Theme
# =============================================================================

# Open the theme file from /res/theme/file.css
# Write file in content /src/static/css/theme.css 
def create_theme(theme_path, file_path):

	with open(theme_path, "r") as file:

		data = file.read()
		file.close()

	with open(file_path, 'w') as file:

		file.write(data)
		file.close()

	if _settings.get_settings_value("debug"):

		print("------------------[THEME]------------------")
		print(f"Chosen theme : {theme_path}")
		print(f"thme path : {file_path}")
		print("----------------[END THEME]----------------\n")

create_theme(
	os.path.join(THEME_PATH, _settings.get_settings_value("theme") + ".css"), 
	os.path.join(STATIC_PATH, "css/theme.css")
	)


# =============================================================================
# Texts
# =============================================================================

# Load all text from the selected language for the login page
def load_login_texts():

	texts = {}
	texts["page_title"] = _language.get_text("login_page_title")
	texts["login_title"] = _language.get_text("login_title")
	texts["identification"] = _language.get_text("identification")
	texts["username"] = _language.get_text("username")
	texts["password"] = _language.get_text("password")
	texts["login"] = _language.get_text("login")
	texts["login_error"] = _language.get_text("login_error")

	if _settings.get_settings_value('debug'):

		print("------------------[TEXTS]------------------")
		print(texts)
		print("----------------[END TEXTS]----------------\n")

	return texts


# Load all texts from the selected language for the commands page
def load_commands_texts():

	texts = {}
	texts["commands_page_title"] = _language.get_text("commands_page_title")
	texts["commands_title"] = _language.get_text("commands_title")
	texts["connectToCansat"] = _language.get_text("connectToCansat")
	texts["encryptData"] = _language.get_text("encryptData")
	texts["startRecording"] = _language.get_text("startRecording")
	texts["seePreviousData"] = _language.get_text("seePreviousData")
	texts["debug"] = _language.get_text("debug")
	texts["running"] = _language.get_text("running")
	texts["capturing"] = _language.get_text("capturing")
	texts["saving"] = _language.get_text("saving")
	texts["wifi"] = _language.get_text("wifi")
	texts["encryption"] = _language.get_text("seePreviousData")
	texts["buzzer"] = _language.get_text("buzzer")
	texts["mode"] = _language.get_text("mode")
	texts["lastData"] = _language.get_text("lastData")
	texts["sensors"] = _language.get_text("sensors")
	texts["camera"] = _language.get_text("camera")
	texts["bmp"] = _language.get_text("bmp")
	texts["accel"] = _language.get_text("accel")
	texts["gps"] = _language.get_text("gps")
	texts["thermalCam"] = _language.get_text("thermalCam")
	texts["humidity"] = _language.get_text("humidity")
	texts["waitingForCansat"] = _language.get_text("waitingForCansat")
	texts["recordingData"] = _language.get_text("recordingData")


	if _settings.get_settings_value('debug'):

		print("------------------[TEXTS]------------------")
		print(texts)
		print("----------------[END TEXTS]----------------\n")

	return texts


# =============================================================================
# Routes
# =============================================================================


# Login view:
# 	- user must be logged to access other views
# 	- username and password are stored at res/settings/auth.json
@APP.route('/', methods=['GET', 'POST'])
def login_view():

	texts = load_login_texts()

	error = None

	with open(os.path.join(SETTINGS_PATH, "auth.json"), 'r') as file:

		auth_data = json.load(file)
		file.close()

	if request.method == 'POST':

		if request.form['username'] != auth_data["username"] or request.form['password'] != auth_data["password"]:

			error = texts["login_error"]
		
		else:

			return redirect(url_for('commands_view'))

	return render_template('login.html', error=error, texts=texts)


# Commands views:
# 	- communicates with the CanSat to send oders and download real-time data. 
@APP.route('/commands', methods=['GET', 'POST'])
def commands_view():

	texts = load_commands_texts()

	js = {}
	js["canSatConnected"] = "disconnected"
	js["switchState"] = ""
	js["recordingState"] = ""
	terminal = {  
			  		"running": "",  
			  		"capturing": "",  
				  	"saving": "",  
				  	"wifi": "",  
				  	"encryption": "",  
				  	"buzzer": "",  
				  	"mode": "",
				  	"last_data": "", 
				  	"sensors": {  
						"camera": "",  
						"bmp": "",  
						"accel": "",  
						"gps": "",  
						"th_cam": "",  
						"humidity": ""  
					}  
				}

	if request.method == 'POST':

		if request.form.get("connectToCansat") != None:

			# try to contact cansat:
			# 	- if failure then try again
			# 	- if success then unlock other functions
			
			while True:

				time.sleep(1)

				# Try to contact Cansat:
				# -	 if error then wait 1s and retry. 
				try:
					c = _api.get_cansat_status()

				except Exception as e:
					
					c = ""

				if c != "":

					break

			terminal = c
			js["canSatConnected"] = "connected"

			return render_template('commands.html', texts=texts, js=js, terminal=terminal)


		elif request.form.get("encryptionSwitch") != None:

			# Enable data encryption
			r = _api.enable_encryption()

			if r != "" or r != False:

				js["canSatConnected"] = "connected"
				js["switchState"] = "checked"

				terminal = _api.get_cansat_status()

				return render_template('commands.html', texts=texts, js=js, terminal=terminal)

			else:

				print("Error or value is not updated ")


		elif request.form.get("startRecord") != None:

			# Start record
			print("STARTING RECORD")
			_api.start_recording()
			js["recordingState"] = "recording"
			
			terminal = _api.get_cansat_status()

			return render_template('commands.html', texts=texts, js=js, terminal=terminal)


		elif request.form.get("stopRecord") != None:

			# Stop recording and redirect to process data pages
			
			_api.stop_recording()
			return redirect(url_for('process_data_view'))


		elif request.form.get("encryptionSwitch") == None:

			# Disable data encryption
			r = _api.disable_encryption()

			if r != "" or r != False:

				js["canSatConnected"] = "connected"
				js["switchState"] = ""

				terminal = _api.get_cansat_status()

				return render_template('commands.html', texts=texts, js=js, terminal=terminal)

			else:

				print("Error or value is not updated ")


		else:

			pass

	return render_template('commands.html', texts=texts, js=js, terminal=terminal)


# Process_data_view:
# 	- web application to process the downloaded data
@APP.route('/process_data')
def process_data_view():
	
	available_data = {}

	folders = os.listdir(os.path.join(DATA_PATH, "normal"))
	available_data["folders"] = folders

	if request.method == 'POST':

		return redirect(url_for("process_data_functions_view", data_set=request.form.get("data")))

	return render_template('process_data.html', available_data=available_data)


# @login_required
@APP.route('/process_data/functions/<int:data_set>')
def process_data_functions_view(data_set):

	pass



# =============================================================================
# Reload
# =============================================================================

# Set new values for all variables
def reload():

	pass


# =============================================================================
# Run program
# =============================================================================


def main():

	APP.run()


if __name__ == '__main__':

	main()