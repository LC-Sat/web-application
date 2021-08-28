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


# =============================================================================
# Routes
# =============================================================================


# Login view:
# 	- user must be logged to access other views
# 	- username and password are stored at res/settings/auth.json
@APP.route('/', methods=['GET', 'POST'])
def login_view():

	theme = _settings.get_settings_value("theme")

	texts = load_login_texts()

	error = None

	with open(os.path.join(SETTINGS_PATH, "auth.json"), 'r') as file:

		auth_data = json.load(file)
		file.close()

	if request.method == 'POST':

		if request.form['username'] != auth_data["username"] or request.form['password'] != auth_data["password"]:

			error = texts["login_error"]
		
		else:

			return redirect(url_for('commands'))

	return render_template('login.html', theme=theme, error=error, texts=texts)


# Commands views:
# 	- communicates with the CanSat to send oders and download real-time data. 
@APP.route('/commands')
def commands_view():
	pass

# Process_data_view:
# 	- web application to process the downloaded data
@APP.route('/process_data')
def process_data_view():
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