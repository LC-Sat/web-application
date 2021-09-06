

# LC-SAT: Web application


Organisation: **[LC-SAT](https://lc-sat.github.io/doc/index)**

Created by [Thomas HODSON](https://www.linkedin.com/in/thomas-hodson-27a465204/), August - September 2021.
Program linked to the CanSat internal software, developped by Aristide URLI.

Project developped with Python 3.9.2 on [Sublime Text](https://www.sublimetext.com/). 

### Project overview

This application was created for the CanSat competition (2020 - 2021), especially for the international phase of the competition. This application process the data recorded by the CanSat during the acsent, the drop and the descent. 

This web-application is an update of the computer software that was created during the national phase of the competition. The purpose is to allow any kind of connected device (which can have access to internet) to process these data. 

## Download

### Dependencies

The project uses the following librairies:

 - os
 - sys
 - subprocess
 - datetime
 - numpy
 - json
 - zipfile
 - shutil
 - time
 - io
 - pickle
 - yaml
 - flask
 - matplotlib
 - opencv
 - folium
 - requests
 
 You can download these librairies with the next command in the terminal (you must run your command in the project root folder):
 

    pip install -r requirements.txt

Notice that the program can automatically download the missing librairies **if** the pip command is available on your computer.

### Run the program

To run the program, you simply have to run the main.py file. When you first run the program, you have to wait a couple of seconds until an URL appears on your terminal. Copy and past the URL in your web browser (I recommand to you firefox or google chrome).

### Errors

- Your program might stop immediatly after you run it without any error on the terminal. It's an importation error which you can find here:

> web-application/logs/webapp/date.txt

  -  The video are not render. When you ask for videos, you have to wait a long time until you can access the video template. If any video are rendered, try to reload the page or consider switching to another web browser. If the thermal video doesn't render, the problem must come from the raw data.

- The custom chart is not render. Reload the page, the web browser must have render the previous chart.  

## Description

The programm runs in two mode: An "online" mode and an "local" mode. 
Both mode starts with the login page:
![Login page](https://cdn.discordapp.com/attachments/845199430688833567/884422621628874812/unknown.png)Note that there are no real login security on this application, you can bypass the authentification with url for instance. This template acts as an idea rather than being a real function. You can find and change the username and the password in the next file:
> web-application/res/settings/auth.json 

Both mode also render the next template:
![enter image description here](https://cdn.discordapp.com/attachments/845199430688833567/884425642861555742/unknown.png)
### Online mode

If you want to communicate with the CanSat you have to click on the "connect to Cansat" checkbox / button. A loading screen is render and it stays until the CanSat is connected to the application. Once the CanSat is connected, the encrypt data switch and the start recording button are unlocked. Once you start the record, a modal appears on you screen with a button to stop the record. 

### Off line mode

On the same template, you can process previous data by clicking the "see previous data" button bellow the command panel.  


Both modes leads to the next template:
![enter image description here](https://cdn.discordapp.com/attachments/845199430688833567/884454034889641984/unknown.png)
The different data sets are stored in indexed files. To load the last recorded data, you have to select the highest number of the list. One you have submit your choice, the application render the next template:
![enter image description here](https://cdn.discordapp.com/attachments/845199430688833567/884455016688132176/unknown.png)
- Maps

The map link first renders a form in which you can apply custom styles on the map. Once you have submited the form  the map appears on your screen.

![enter image description here](https://cdn.discordapp.com/attachments/845199430688833567/884456859275235348/unknown.png)
- Charts

As the map link does, the charts link first leads to a form. On this form you have to select which data you want to use in your chart. If you want to plot multiple data, multiple charts are created. You can select custom titles and lables but the application can create automatically those texts.
![enter image description here](https://media.discordapp.net/attachments/845199430688833567/884457674983489606/unknown.png?width=1374&height=670)   ![enter image description here](https://media.discordapp.net/attachments/845199430688833567/884457822522327061/unknown.png?width=1379&height=670)
- Videos

The video links might take some time (several minutes) to render the template. Two videos are displayed on the screen once the template is rendered.

To access the settings template, you have to enter the following url :
> localhost:5000/settings/

A form is displayed on the screen. This functionnallity might occured some problems with the reloading system. In case of any bug, you might re-download all the settings files. 

![enter image description here](https://media.discordapp.net/attachments/845199430688833567/884458851611574292/unknown.png?width=1376&height=670)

## Configuration

This application uses different config files in the next folder:
> web-application/res/settings/

- **settings.yaml**

This file contains the general settings of the app. 
```yaml
theme: dark
language: en-us
cansatIp: http://127.0.0.1
debug: true
```
- **urls.json**

This file contains the urls paterns for the API.
```json
{
	"status": "/api/cansat/status",
	"download": "/api/download",
	"start_recording": "/api/capture/start",
	"stop_recording": "/api/capture/stop",
	"start_encryption": "/api/encryption/start",
	"stop_encryption": "/api/encryption/stop",
	"start_buzzer": "/api/buzzer/start",
	"stop_buzzer": "/api/buzzer/stop",
	"shutdown": "/api/cansat/shutdown",
	"shutdown_status": "/api/cansat/status/shutdown",
	"logs": "/api/cansat/logs"
}
```

- **auth.json**

This file contains the username and the password for the login template.
```json
{
	"username": "the_username",
	"password": "the_password"
}
```
- **charts.json**
This file contains the default configuration settings for the charts.
```json
{
	"recordingFrequency": 0.3,
	"defaultPointStyle": ".",
	"pointsType": [
		"",
		".",
		",",
		"o",
		"v",
		"^",
		"<",
		">"	
	],
	"defaultLineStyle": "-",
	"linesType": [
		"-",
		"--",
		"-.",
		":"
	],
	"defaultLineWidth": 1,
	"data_config": {
		"press": {	
			"name": "pression",
			"unit": "hPa",
			"prefix": "press"
		},
		"temp":{
			"name": "temperature",
			"unit": "°C",
			"prefix": "temp"
		},
		"alt": {
			"name": "altitude",
			"unit": "m",
			"prefix": "alt"
		},
		"hum": {
			"name": "humidity",
			"unit": "",
			"prefix": "hum"
		},
		"ax": {
			"name": "x_acceleration",
			"unit": "N",
			"prefix": "ax"
		},
		"ay": {
			"name": "y_acceleration",
			"unit": "N",
			"prefix": "ay"
		},
		"az": {
			"name": "z_acceleration",
			"unit": "N",
			"prefix": "az"
		},
		"speed": {
			"name": "velocity",
			"unit": "m/s",
			"prefix": "speed"
		},
		"qual": {
			"name": "signal_quality",
			"unit": "",
			"prefix": "qual"
		},
		"sat": {
			"name": "satellites",
			"unit": "",
			"prefix": "sat"
		}
	},
	"nameToPrefix": {
		"pression": "press",
		"pressure": "press",
		"temperature": "temp",
		"température": "temp",
		"altitude": "alt",
		"humidity": "hum",
		"humidité": "hum",
		"x_acceleration": "ax",
		"x_accélération": "ax",
		"y_acceleration": "ay",
		"y_accélération": "ay",
		"z_accélération": "az",
		"velocity": "speed",
		"vitesse": "speed",
		"satellites": "sat"
	},
	"defaultColor": "#000000"
}	
```

- **maps.json**

This file contains the default configuration settings for the maps:
```json
{
	"defaultTitle": "cansatPositions",
	"defaultZoom": 15,
	"defaultIcon": "map-marker",
	"icons": [
		"asterisk",
		"plus",
		"euro",
		"eur",
		....
	],
	"icon_default_color": "yellow",
	"iconsColor": [
		"red",
		"blue", 
		"green",
		"purple",
		"orange",
		"darkred",
    "lightred",
    "beige",
    "darkblue",
    "darkgreen",
    "cadetblue",
    "darkpurple",
    "white",
    "pink",
    "lightblue",
    "lightgreen",
    "gray",
    "black",
    "lightgray"
    ],
	"tiles": [
		"Stamen Toner",
		"Stamen Terrain",
		"openstreetmap",
		"stamenwatercolor"
	]
}
```

- **video.json**
 
 This file contains the default configuration settings for videos.
```json
{
	"videoSize": 640,
	"FPS": 30,
	"minimalTemperature": -40,
	"maximalTemperature": 85,
	"minimalColor": [0, 0, 255],
	"mediumColor": [0, 255, 0],
	"maximalColor": [255, 0, 0]
}
``` 
 
## Notes

Note that:
- You can't change the default colors for the thermal camera (in the video.json file).
- The thermal camera video might not work (depends on recorded data). 
- The thermal camera resolution is very low  (original resolution is 8 x 8 pixels).  
- You can add other tiles to the map config file but they might required an internet access to be rendered.
- You can't add other icons because for the maps.

The templates are coded for any kind of device (from smartphones to computers).  


> Written with [StackEdit](https://stackedit.io/).
