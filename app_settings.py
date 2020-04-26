"""
Contains all the Flask App Settings
"""
import os
import json
import datetime as dt
from flask import Flask
from flask_restful import Api
from logger import get_logger


# App Constants
APP_NAME = "CARE"
ROOT = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(ROOT, 'input')
BUILD_FOLDER = os.path.join(ROOT, 'build')
OUTPUT_FOLDER = os.path.join(ROOT, 'output')
LOG_FOLDER = os.path.join(ROOT, 'logs')
LOG_FILE_NAME = 'APP_' + dt.datetime.now().strftime("%Y%m%d_%H%M") + '.log'
LOG_FILE = os.path.join(LOG_FOLDER, LOG_FILE_NAME)

# App Settings
APP = Flask(__name__)
APP.secret_key = "**********"
APP.config['INPUT_FOLDER'] = INPUT_FOLDER
APP.config['BUILD_FOLDER'] = BUILD_FOLDER
APP.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
APP.config['USERS'] = json.load(open('users.json'))
APP.static_folder = 'static'
APP.logger = get_logger(__name__, level='debug', log_file=LOG_FILE)
API = Api(APP)
