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

_api = Api(
	DEBUG,
	_settings.get_settings_value("cansatIp"),
	SETTINGS_PATH,
	os.path.join(LOG_PATH, "cansat/"),
	DATA_PATH
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

_video = Video(
	DEBUG,
	STATIC_PATH,
	SETTINGS_PATH
	)


if _settings.get_settings_value("debug"):

	print("------------------[DEBUG]------------------")
	print(f"DEBUG | {_settings}\t OK")
	print(f"DEBUG | {_language}\t OK")
	print(f"DEBUG | {_api}\t      OK")
	print(f"DEBUG | {_map}\t      OK")
	print(f"DEBUG | {_chart}\t      OK")
	print(f"DEBUG | {_video}\t      OK")
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
# Reload
# =============================================================================


# Set new values for all variables
def reload_general_settings(theme, language, debug, cansatIp):

	# rewriting settings
	with open(os.path.join(SETTINGS_PATH, "settings.yaml"), 'r', encoding = "utf-8") as file:

		data = yaml.load(file)
		file.close()

	data["theme"] = theme
	data["language"] = language
	data["debug"] = debug
	data["cansatIp"] = cansatIp

	with open(os.path.join(SETTINGS_PATH, "settings.yaml"), 'w', encoding = "utf-8") as file:

		d = yaml.dump(data, file)
		file.close()

	# reloading Setting class + language class + rewriting style
	_settings.reload(os.path.join(SETTINGS_PATH, "settings.yaml"))
	_language.reload(os.path.join(LANGUAGE_FOLDER, _settings.get_settings_value("language") + ".json"), _settings.get_settings_value("debug"))
	create_theme(os.path.join(THEME_PATH, _settings.get_settings_value("theme") + ".css"), os.path.join(STATIC_PATH, "css/theme.css"))


	if _settings.get_settings_value("debug"):

		print("------------------[RELOAD]------------------")
		print(f"DEBUG | {data}\t OK")

	return


def reload_api(self, api_status, api_download, api_start_recording, api_stop_recording, api_start_encryption, api_stop_encryption, api_start_buzzer, api_stop_buzzer, api_shutdown, api_shutdown_status, api_logs):

	# rewriting api config
	with open(os.path.join(SETTINGS_PATH, "urls.json"), 'r', encoding = "utf-8") as file:

		api_data = json.load(file)
		file.close()

	api_data["status"] = api_status
	api_data["download"] = api_download
	api_data["start_recording"] = api_start_recording
	api_data["stop_recording"] = api_stop_recording
	api_data["start_encryption"] = api_start_encryption
	api_data["stop_encryption"] = api_stop_encryption
	api_data["start_buzzer"] = api_start_buzzer
	api_data["stop_buzzer"] = api_stop_buzzer
	api_data["shutdown"] = api_shutdown
	api_data["shutdown_status"] = api_shutdown_status
	api_data["logs"] = api_logs

	# Writing new settings
	with open(os.path.join(SETTINGS_PATH, "urls.json"), 'w', encoding = "utf-8") as file:

		json.dump(api_data, file, sort_keys = True, indent = 4)
		file.close()

	_api.reload(_settings.get_settings_value("debug"), _settings.get_settings_value("cansatIp"), SETTINGS_PATH)

	if _settings.get_settings_value("debug"):

		print("------------------[RELOAD]------------------")
		print(f"DEBUG | {api_data}")

	return


def reload_charts(recording_frequency, default_point_style, default_line_style, default_line_style_color, data_config):

	with open(os.path.join(SETTINGS_PATH, "charts.json"), 'r', encoding = "utf-8") as file:

		chart_data = json.load(file)
		file.close()

	chart_data["recordingFrequency"] = recording_frequency
	chart_data["defaultPointStyle"] = default_point_style
	chart_data["defaultLineStyle"] = default_line_style
	chart_data["defaultColor"] = default_line_style_color
	chart_data["data_config"] = data_config

	# Writing new settings
	with open(os.path.join(SETTINGS_PATH, "charts.json"), 'r', encoding = "utf-8") as file:

		json.dump(chart_data, file, sort_keys = True, indent = 4)
		file.close()

	_chart.reload(_settings.get_settings_value("debug"), os.path.join(SETTINGS_PATH, "charts.json"))

	if _settings.get_settings_value("debug"):

		print(f"DEBUG | {chart_data}")

	return


def reload_maps(map_title, map_zoom_start, map_default_marker, map_default_marker_color):

	with open(os.path.join(SETTINGS_PATH, "maps.json"), 'r', encoding = "utf-8") as file:

		map_data = json.load(file)
		file.close()

	map_data["defaultTitle"] = map_title
	map_data["defaultZoom"] = map_zoom_start
	map_data["defaultIcon"] = map_default_marker
	map_data["icon_default_color"] = map_default_marker_color

	# Writing new settings
	with open(os.path.join(SETTINGS_PATH, "maps.json"), 'w', encoding = "utf-8") as file:

		json.dump(map_data, file , sort_keys = True, indent = 4)
		file.close()

	_map.reload(_settings.get_settings_value("debug"), os.path.join(SETTINGS_PATH, "maps.json"))

	if _settings.get_settings_value("debug"):

		print(f"DEBUG | {map_data}")

	return


def reload_videos(video_size, fps, minimal_temperature, maximal_temperature):

	with open(os.path.join(SETTINGS_PATH, "video.json"), "r", encoding = "utf-8") as file:

		video_data = json.load(file)
		file.close()

	video_data["videoSize"] = video_size	
	video_data["FPS"] = fps	
	video_data["minimalTemperature"] = minimal_temperature
	video_data["maximalTemperature"] = maximal_temperature

	# Writing new settings
	with open(os.path.join(SETTINGS_PATH, "video.json"), "w", encoding = "utf-8") as file:

		json.dump(video_data, file, sort_keys = True, indent = 4)
		file.close()

	_chart.reload(_settings.get_settings_value("debug"), os.path.join(SETTINGS_PATH, "video.json"))

	if _settings.get_settings_value("debug"):

		print(f"DEBUG | {video_data}")
		print("----------------[END RELOAD]----------------\n")

	return


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


# Load all texts from the selected language for the chose data set page
def load_chose_data_set_texts():

	texts = {}
	texts["selectDatasetPageTitle"] = _language.get_text("selectDatasetPageTitle")
	texts["selectDataSet"] = _language.get_text("selectDataSet")
	texts["submit"] = _language.get_text("submit")

	if _settings.get_settings_value('debug'):

		print("------------------[TEXTS]------------------")
		print(texts)
		print("----------------[END TEXTS]----------------\n")


	return texts


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


# Load all texts from the selected language for the settings view
def load_settings_texts():

	texts = {}
	texts["settingsPageTitle"] = _language.get_text("settingsPageTitle")
	texts["generalSettings"] = _language.get_text("generalSettings")
	texts["settingsDebugMode"] = _language.get_text("settingsDebugMode")
	texts["languages"] = _language.get_text("languages")
	texts["themes"] = _language.get_text("themes")
	texts["cansatSettings"] = _language.get_text("cansatSettings")
	texts["urlBase"] = _language.get_text("urlBase")
	texts["apiUrls"] = _language.get_text("apiUrls")
	texts["apiDoc"] = _language.get_text("apiDoc")
	texts["here"] = _language.get_text("here")
	texts["chartSettings"] = _language.get_text("chartSettings")
	texts["recordingFrequency"] = _language.get_text("recordingFrequency")
	texts["selectPointStyle"] = _language.get_text("selectPointStyle")
	texts["selectLineStyle"] = _language.get_text("selectLineStyle")
	texts["dataConfig"] = _language.get_text("dataConfig")
	texts["lineColor"] = _language.get_text("lineColor")
	texts["mapSettings"] = _language.get_text("mapSettings")
	texts["mapTitle"] = _language.get_text("mapTitle")
	texts["mapZoom"] = _language.get_text("mapZoom")
	texts["mapMarker"] = _language.get_text("mapMarker")
	texts["mapMarkerColor"] = _language.get_text("mapMarkerColor")
	texts["videoSettings"] = _language.get_text("videoSettings")
	texts["videoSettingsSize"] = _language.get_text("videoSettingsSize")
	texts["videoSettingsMinimalTemperature"] = _language.get_text("videoSettingsMinimalTemperature")
	texts["videoSettingsMaximalTemperature"] = _language.get_text("videoSettingsMaximalTemperature")
	texts["videoSettingsFPS"] = _language.get_text("videoSettingsFPS")
	texts["submit"] = _language.get_text("submit")
	texts["settingsTemperatureError"] = _language.get_text("settingsTemperatureError")

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
@APP.route('/', methods = ['GET', 'POST'])
def login_view():

	texts = load_login_texts()

	error = None

	with open(os.path.join(SETTINGS_PATH, "auth.json"), 'r', encoding = "utf-8") as file:

		auth_data = json.load(file)
		file.close()

	if request.method == 'POST':

		if request.form['username'] != auth_data["username"] or request.form['password'] != auth_data["password"]:

			error = texts["login_error"]
		
		else:

			return redirect(url_for('commands_view'))

	return render_template('login.html', error = error, texts = texts)


# Commands views:
# 	- communicates with the CanSat to send oders and download real-time data. 
@APP.route('/commands', methods = ['GET', 'POST'])
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

			return render_template('commands.html', texts = texts, js = js, terminal = terminal)


		elif request.form.get("encryptionSwitch") != None:

			# Enable data encryption
			r = _api.enable_encryption()

			if r != "" or r != False:

				js["canSatConnected"] = "connected"
				js["switchState"] = "checked"

				terminal = _api.get_cansat_status()

				return render_template('commands.html', texts = texts, js = js, terminal = terminal)

			else:

				print("Error or value is not updated ")


		elif request.form.get("startRecord") != None:

			# Start record
			print("STARTING RECORD")
			_api.start_recording()
			js["recordingState"] = "recording"
			
			terminal = _api.get_cansat_status()

			return render_template('commands.html', texts = texts, js = js, terminal = terminal)


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

				return render_template('commands.html', texts = texts, js = js, terminal = terminal)

			else:

				print("Error or value is not updated ")

		else:

			pass

	return render_template('commands.html', texts = texts, js = js, terminal = terminal)


# Process_data_view:
# 	- web application to process the downloaded data
# 	USer select the data set
@APP.route('/process_data', methods = ['GET', 'POST'])
def process_data_view():
	
	available_data = {}
	texts = load_chose_data_set_texts()

	folders = os.listdir(os.path.join(DATA_PATH, "normal"))
	available_data["folders"] = folders

	if request.method == 'POST':

		data_set = int(request.form.get("data"))

		return redirect(url_for("process_data_functions_view", data_set = data_set))

	return render_template('process_data.html', available_data = available_data, texts = texts)


# Links to different data processing functions
@APP.route('/process_data/functions/<int:data_set>', methods = ['GET', 'POST'])
def process_data_functions_view(data_set):

	texts = load_process_data_functions_texts()
	data = {}
	data['set'] = str(data_set)
	
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

	_video.render_classic_video(os.path.join(DATA_PATH, "normal/" + str(data_set)))
	_video.render_thermal_video(os.path.join(DATA_PATH, "normal/" + str(data_set)))

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


# The settings view
@APP.route("/settings", methods = ['GET', 'POST'])
def settings_view():

	# Load texts in selected language
	texts = load_settings_texts()
	

	# Load general settings for default value in form
	general_settings = {}
	general_settings["debugMode"] = _settings.get_settings_value("debug")

	languages = os.listdir(LANGUAGE_FOLDER)
	for i, language in enumerate(languages):

		languages[i] = language.replace(".json", "")

	general_settings["languages"] = languages

	themes = os.listdir(THEME_PATH)
	for i, theme in enumerate(themes):

		themes[i] = theme.replace(".css", "")

	general_settings["themes"] = themes

	# Load cansat settings for default value in form
	cansat_settings = {}
	cansat_settings["urlBase"] = _settings.get_settings_value("cansatIp")
	urls_patterns = []

	with open(os.path.join(SETTINGS_PATH, "urls.json"), 'r', encoding = "utf-8") as f:

		urls = json.load(f)
		f.close()

	for key, value in urls.items():

		urls_patterns.append([key, value])

	cansat_settings["urlsPatterns"] = urls_patterns

	# Load chart settings for default value in form
	chart_settings = {}

	with open(os.path.join(SETTINGS_PATH, "charts.json"), 'r', encoding = "utf-8") as f:

		chart_conf = json.load(f)
		f.close()

	chart_settings["recordingFrequency"] = chart_conf["recordingFrequency"]
	chart_settings["defaultPointStyles"] = chart_conf["pointsType"]
	chart_settings["defaultLineStyles"] = chart_conf["linesType"]

	data_config = []
	for key, value in chart_conf["data_config"].items():

		data_config.append(value)

	chart_settings["dataConfig"] = data_config
	chart_settings["defaultLineColor"] = chart_conf["defaultColor"]

	# Load general settings for default value in form
	map_settings = {}

	with open(os.path.join(SETTINGS_PATH, "maps.json"), 'r', encoding = "utf-8") as f:

		map_conf = json.load(f)
		f.close()

	map_settings["mapTitle"] = map_conf["defaultTitle"]
	map_settings["defaultZoom"] = map_conf["defaultZoom"]
	map_settings["defaultMarker"] = map_conf["icons"]
	map_settings["defaultMarkerColor"] = map_conf["iconsColor"]

	# Load video settings for default value in form
	video_settings = {}

	with open(os.path.join(SETTINGS_PATH, "video.json"), 'r', encoding = "utf-8") as f:

		video_config = json.load(f)
		f.close()

	video_settings["videoSize"] = video_config["videoSize"]
	video_settings["minimalTemperature"] = video_config["minimalTemperature"]
	video_settings["maximalTemperature"] = video_config["maximalTemperature"]
	video_settings["FPS"] = video_config["FPS"]


	if request.method == 'POST':

		# General settings reload

		selected_theme = request.form.get("theme")
		selected_language = request.form.get("languages")

		if request.form.get("debug") == None:

			selected_debug_mode = False

		else:

			selected_debug_mode = True

		selected_url_root = request.form.get("urlBase")

		reload_general_settings(
			selected_theme,
			selected_language,
			selected_debug_mode,
			selected_url_root
			)

		# API settings relaod
		selected_api_status = request.form.get("statusUrlInput") 
		selected_api_download = request.form.get("downloadUrlInput") 
		selected_api_start_recording = request.form.get("start_recordingUrlInput")
		selected_api_stop_recording = request.form.get("stop_recordingUrlInput")
		selected_api_start_encryption = request.form.get("start_encryptionUrlInput")
		selected_api_stop_encryption = request.form.get("stop_encryptionUrlInput")
		selected_api_start_buzzer = request.form.get("start_buzzerUrlInput")
		selected_api_stop_buzzer = request.form.get("stop_buzzerUrlInput")
		selected_api_shutdown = request.form.get("shutdownUrlInput")
		selected_api_shutdown_status = request.form.get("shutdown_statusUrlInput")
		selected_api_logs = request.form.get("logsUrlInput")
		
		reload_api(
			selected_api_status,
			selected_api_download,
			selected_api_start_recording, 
			selected_api_stop_recording,
			selected_api_start_encryption,
			selected_api_stop_encryption, 
			selected_api_start_buzzer,
			selected_api_stop_buzzer,
			selected_api_shutdown,
			selected_api_shutdown_status, 
			selected_api_logs
			)

		# Chart settings reload
		
		selected_chart_recording_frequency = request.form.get("recordingFrequency")
		selected_chart_point_style = request.form.get("pointStyle")
		selected_chart_line_style = request.form.get("lineStyle")
		selected_chart_line_color = request.form.get("defaultLineColor")

		with open(os.path.join(SETTINGS_PATH, "charts.json"), "r", encoding = "utf-8") as file:

			chart_data = json.load(file)
			file.close()

		data_config = {}

		for key, value in chart_data["data_config"]:

			dic = {}
			dic["name"] = value["name"]
			dic["unit"] = request.form.get(dic["name"] + "Unit")
			dic["prefix"] = value["prefix"]

			data_config[key] = dic
		
		reload_charts(
			selected_chart_recording_frequency,
			selected_chart_point_style,
			selected_chart_line_style,
			selected_chart_line_color,
			data_config
			)

		# Map settings relaod

		selected_map_title = request.form.get("mapTitle")
		selected_default_zoom = request.form.get("defaultZoom")
		selected_default_marker = request.form.get("defaultMarker")
		selected_default_marker_color = request.form.get("defaultMarkerColor")

		reload_maps(
			selected_map_title,
			selected_default_zoom,
			selected_default_marker,
			selected_default_marker_color
			)

		# video settings reload

		selected_video_size = request.form.get("videoSize")
		selected_video_fps = request.form.get("FPS")
		selected_video_minimal_temperature = request.form.get("minimalTemperature")
		selected_video_maximal_temperature = request.form.get("maximalTemperature")

		reload_videos(
			selected_video_size,
			selected_video_fps,
			selected_video_minimal_temperature,
			selected_video_maximal_temperature
			)

		return redirect(url_for("process_data_view"))

	return render_template("settings.html", texts = texts, general_settings = general_settings, cansat_settings = cansat_settings, chart_settings = chart_settings, map_settings = map_settings, video_settings = video_settings)


# =============================================================================
# Run program
# =============================================================================


def main():

	APP.run()


if __name__ == '__main__':

	main()