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
	log_name = str(date.today().strftime("%b-%d-%Y") + ".txt")

	with open(os.path.join(log_path, log_name), "a", encoding = "utf-8") as log:

		log.write('\n' + str(text) + '\n')
		log.close()

	return


def install_packages():

	try:
		file_path = os.path.join(BASE_DIR, "requirements.txt")
		subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", file_path])

	except Exception as e:

		log(e)

		sys.exit()

	return


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
		log_name = str(date.today().strftime("%b-%d-%Y") + ".txt")

		log(e)

		sys.exit()


# =============================================================================
# Local imports
# =============================================================================


try:
	from scripts.graphs import Chart
	from scripts.maps import Map

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
APP.config['UPLOAD_FOLDER'] = "media/"


# =============================================================================
# Controllers class
# =============================================================================


# Settings class

class Settings:


	def __init__(self, file_path):

		self.debug = False

		with open(file_path, 'r', encoding = "utf-8") as file:

			self.settings_data = yaml.load(file)

			file.close()

		return


	def __str__(self):

		return "Settings class"


	def reload(self, file_path):

		with open(file_path, 'r', encoding = "utf-8") as file:

			self.settings_data = yaml.load(file)

			file.close()

		self.debug = self.get_settings_value("debug")

		return

	
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

		with open(file_path, 'r', encoding = "utf-8") as file:

			self.language_data = json.load(file)

			file.close()

		return


	def __str__(self):

		return "Language class"


	def reload(self, file_path, debug):

		with open(file_path, 'r', encoding = "utf-8") as file:

			self.language_data = json.load(file)

			file.close()

		self.debug = debug

		return


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

DEBUG = _settings.get_settings_value("debug")

_language = Language(
	DEBUG,
	LANGUAGE_FOLDER + _settings.get_settings_value("language") + ".json"
	)

_map = Map(
	DEBUG,
	os.path.join(SETTINGS_PATH, "maps.json")
	)

_chart = Chart(
	DEBUG,
	os.path.join(SETTINGS_PATH, "charts.json"),
	os.path.join(STATIC_PATH, "result/"),
	_language
	)


if _settings.get_settings_value("debug"):

	print("------------------[DEBUG]------------------")
	print(f"DEBUG | {_settings}\t OK")
	print(f"DEBUG | {_language}\t OK")
	print(f"DEBUG | {_map}\t      OK")
	print(f"DEBUG | {_chart}\t      OK")
	print("----------------[END DEBUG]----------------\n")


# =============================================================================
# Theme
# =============================================================================


# Open the theme file from /res/theme/file.css
# Write file in content /src/static/css/theme.css 
def create_theme(theme_path, file_path):

	with open(theme_path, "r", encoding = "utf-8") as file:

		data = file.read()
		file.close()

	with open(file_path, 'w', encoding = "utf-8") as file:

		file.write(data)
		file.close()

	if _settings.get_settings_value("debug"):

		print("------------------[THEME]------------------")
		print(f"Chosen theme : {theme_path}")
		print(f"thme path : {file_path}")
		print("----------------[END THEME]----------------\n")

	return


create_theme(
	os.path.join(THEME_PATH, _settings.get_settings_value("theme") + ".css"), 
	os.path.join(STATIC_PATH, "css/theme.css")
	)


# =============================================================================
# Texts
# =============================================================================



# Load all texts from the selected language for the select process data function
def load_process_data_functions_texts():

	texts = {}
	texts["processDataFunctionsPageTitle"] = _language.get_text("processDataFunctionsPageTitle")
	texts["maps"] = _language.get_text("maps")
	texts["videos"] = _language.get_text("videos")
	texts["charts"] = _language.get_text("charts")

	if _settings.get_settings_value('debug'):

		print("------------------[TEXTS]------------------")
		print(texts)
		print("----------------[END TEXTS]----------------\n")

	return texts


# Load all texts from the selected language for the map view
def load_map_texts():

	texts = {}
	texts["mapPageTitle"] = _language.get_text("mapPageTitle")
	texts["mapTitle"] = _language.get_text("mapTitle")
	texts["iconsColor"] = _language.get_text("iconsColor")
	texts["selectIcon"] = _language.get_text("selectIcon")
	texts["selectZoomStart"] = _language.get_text("selectZoomStart")
	texts["submit"] = _language.get_text("submit")

	if _settings.get_settings_value('debug'):

		print("------------------[TEXTS]------------------")
		print(texts)
		print("----------------[END TEXTS]----------------\n")

	return texts


# Load all texts from the selected language for the video view
def load_video_texts():

	texts = {}
	texts["videoPageTitle"] = _language.get_text("videoPageTitle")
	texts["videoRenderError"] = _language.get_text("videoRenderError")
	texts["thermalVideoRenderError"] = _language.get_text("thermalVideoRenderError")

	if _settings.get_settings_value('debug'):

		print("------------------[TEXTS]------------------")
		print(texts)
		print("----------------[END TEXTS]----------------\n")

	return texts


# Load all texts from the selected language for the chart view
def load_chart_texts():

	texts = {}
	texts["chartPageTitle"] = _language.get_text("chartPageTitle")
	texts["chartTitle"] = _language.get_text("chartTitle")
	texts["chartXLabel"] = _language.get_text("chartXLabel")
	texts["chartYLabel"] = _language.get_text("chartYLabel")
	texts["chartSelectData"] = _language.get_text("chartSelectData")
	texts["chartlineWidth"] = _language.get_text("chartlineWidth")
	texts["chartSubmit"] = _language.get_text("chartSubmit")

	if _settings.get_settings_value('debug'):

		print("------------------[TEXTS]------------------")
		print(texts)
		print("----------------[END TEXTS]----------------\n")

	return texts


# =============================================================================
# Routes
# =============================================================================


# Links to different data processing functions
@APP.route('/', methods = ['GET', 'POST'])
def process_data_functions_view():

	texts = load_process_data_functions_texts()
	data = {}
	data['set'] = "0"
	
	return render_template('process_index.html', texts = texts, data = data)


# First render a form then render in a new window a map with different tyles and markers
@APP.route("/process_data/map/<data_set>", methods = ['GET', 'POST'])
def process_data_map_view(data_set):

	# Load default values in form
	with open(os.path.join(SETTINGS_PATH, "maps.json"), "r", encoding = "utf-8") as file:

		map_config = json.load(file)
		file.close()

	texts = load_map_texts()

	default_data = {}
	default_data["mapTitle"] = map_config['defaultTitle']
	default_data["iconsColor"] = map_config['iconsColor']
	default_data["defaultIconsColor"] = map_config['icon_default_color']
	default_data["defaultIcon"] = map_config["defaultIcon"]
	default_data["icons"] = map_config["icons"]
	default_data["zoomStart"] = map_config["defaultZoom"]

	# Create the map with the selected values
	if request.method == 'POST':

		with open(os.path.join(DATA_PATH, "normal/" + str(data_set)) + "/data.bin", "rb") as file:

			data =  pickle.load(file)
			file.close()

		_map.create_map(
			data["lat"],
			data["lon"],
			str(request.form.get("mapTitle")),
			str(request.form.get("iconTypes")),
			str(request.form.get("iconsColor")),
			int(request.form.get("zoomStart")),
			os.path.join(BASE_DIR, 'src/templates/')
			)

		return render_template("map.html")

	return render_template("maps.html", texts = texts, default_data = default_data)


# Render the classic and the thermal video
@APP.route("/process_data/video/<data_set>", methods = ['GET', 'POST'])
def process_data_video_view(data_set):

	texts = load_video_texts()

	return render_template("video.html", texts = texts)


# First render a form then create the graph 
@APP.route("/process_data/chart/<data_set>", methods = ['GET', 'POST'])
def process_data_chart_view(data_set):

	texts = load_chart_texts()

	# load default values in the form
	with open(os.path.join(DATA_PATH, "normal/" + str(data_set)) + "/data.bin", "rb") as file:

		data =  pickle.load(file)
		file.close()

	with open(os.path.join(SETTINGS_PATH, 'charts.json'), "r") as file:

		data_config = json.load(file)
		file.close()

	chart_config = {}
	chart_config["pointsType"] = data_config["pointsType"]
	chart_config["linesType"] = data_config["linesType"]
	chart_config["defaultLineWidth"] = data_config["defaultLineWidth"]
	chart_config["defaultColor"] = data_config["defaultColor"]
		
	x_data = {}
	x_data["data"] = []

	y_data = {}
	y_data["data"] = []

	for d in data.keys():

		try:

			x_data["data"].append(data_config["data_config"][d])
			y_data["data"].append(data_config["data_config"][d])

		except KeyError:

			pass

	time = {"name": "time", "unit": "s", "prefix": "time"}
	x_data["data"].append(time)

	# Loading all users choices and create chart

	if request.method == 'POST':

		chart_title = request.form["chartTitle"]
		line_width = request.form.get("lineWidth")
		
		# Getting the abscisses value

		Xdata = []
		
		if request.form.get("xData") == "time":

			Xdata.append({"name": "time", "values": [], "prefix": "time", "unit": "0.3s"})
		
		else:

			dic = {}
			dic["name"] = request.form.get("xData")
			dic["prefix"] = data_config["data_config"][data_config["nameToPrefix"][dic["name"]]]["prefix"]
			prefix = data_config["data_config"][data_config["nameToPrefix"][dic["name"]]]["prefix"]
			dic["values"] = data[prefix]
			dic["unit"] = data_config["data_config"][dic["prefix"]]["unit"]
			Xdata.append(dic)
 
		# Getting the ordonates value
		yValues = []

		for d in data.keys():

			try:

				if request.form.get(data_config["data_config"][d]["name"]) != None and data_config["data_config"][d] not in Xdata:

					yValues.append(d)

			except KeyError:

				pass

		Ydata = []

		for value in yValues:

			dic = {}
			dic["name"] = data_config["data_config"][value]["name"]
			dic["prefix"] = value
			dic["values"] = data[value]
			dic["color"] = request.form.get(data_config["data_config"][value]["name"] + "Color")
			dic["point"] = request.form.get(data_config["data_config"][value]["name"] + "PointStyle")
			dic["line"] = request.form.get(data_config["data_config"][value]["name"] + "LineStyle")
			dic["legend"] = request.form.get(data_config["data_config"][value]["name"] + "Legend")
			dic["unit"] = data_config["data_config"][value]["unit"]
			
			Ydata.append(dic)

		if request.form["chartYLabel"] == "" or request.form["chartYLabel"] == None:

			x_label = ""

		else:

			x_label = request.form["chartXLabel"]

		if request.form["chartYLabel"] == "" or request.form["chartYLabel"] == None:

			y_label = ""

		else:

			y_label = request.form["chartYLabel"]

		_chart.draw_chart(Xdata, Ydata, chart_title, x_label, y_label, line_width)

		return render_template("chart.html")

	return render_template("charts.html", texts = texts, y_data = y_data, x_data = x_data, chart_config = chart_config)


# =============================================================================
# Run program
# =============================================================================


def main():

	APP.run()


if __name__ == '__main__':

	main()