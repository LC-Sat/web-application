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
import numpy
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Runs pip install -r requirements.txt
# 	- if importation error:
# 		- log errors
# 		- terminate script

def log(text):

	log_path = os.path.join(BASE_DIR, "logs")
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
	from flask import Flask
	import matplotlib.pyplot as plt

except Exception as e:
	install_packages()

finally:

	try:
		from flask import Flask
		import matplotlib.pyplot as plt

	except Exception as e:

		log_path = os.path.join(BASE_DIR, "logs")
		log_name = str(date.today().strftime("%b-%d-%Y")+".txt")

		log(e)

		sys.exit()


# =============================================================================
# Local imports
# =============================================================================


try:
	pass

except Exception as e:

	log(e)
	sys.exit()


# =============================================================================
# Consts
# =============================================================================


TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'res/templates')
SETTINGS_FOLDER = os.path.join(BASE_DIR, 'res/settings')
LANGUAGE_FOLDER = os.path.join(BASE_DIR, 'res/i18n')
APP = Flask(__name__)


# =============================================================================
# Controllers class
# =============================================================================


# Settings class

class Settings:


	def __init__(self, file_path):

		with open(file_path, 'r') as file:

			self.settings_data = yaml.load(file)

			file.close()


	def __str__(self):

		return "Settings class"

	
	def return_settings_value(self, value):
		
		return str(self.settings_data["settings"][value])


# Language class

class Language:


	def __init__(self, file_path):

		with open(file_path, 'r') as file:

			self.language_data = json.load(file)

			file.close()


	def __str__(self):

		return "Language class"


	def return_text(self, text):

		return self.language_data[text]

# =============================================================================
# Routes
# =============================================================================


# Login view:
# 	- user must be logged to access other views
@APP.route('/')
def login_view():
	pass


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
# Run program
# =============================================================================


def main():

	print("start")
	APP.run()

# if __name__ == '__main__':

# 	main()