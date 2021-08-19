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