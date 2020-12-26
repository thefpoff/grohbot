from flask import Flask, render_template
import time
import os
import datetime
import pickle
import csv
from TempHumMeasurements import TempHumMeasurements
from GrohbotConfig import GrohbotConfig
from flask import request

app = Flask(__name__)


def save_device_states_to_file(devices):

    # file for saving/pickle 
    file = open('pickles/devices_states.pkl', 'wb')
    pickle.dump(devices, file)
    file.close()

def save_config_to_file(grohbotconfig):

    # file for saving/pickle 
    file = open('pickles/grohbotconfig.pkl', 'wb')
    pickle.dump(grohbotconfig, file)
    file.close()

def get_config_from_file():

    # open the file where data is dumped
    fileo = open('pickles/grohbotconfig.pkl', 'rb')
    datao = pickle.load(fileo)
    fileo.close()

    return datao

def page_stuff():

	# open the file where data is dumped
	fileo = open('pickles/temphum.pkl', 'rb')
	temps = pickle.load(fileo)
	fileo.close()

	# open the file where data is dumped
	fileo = open('pickles/devices_states.pkl', 'rb')
	devices = pickle.load(fileo)
	fileo.close()
	
	configdata = get_config_from_file()
	return temps, devices, configdata

def take_pic(tempf, humidity):
	
	take_pic_command = 'fswebcam -r 640x480 -S 30 -F 10 --quiet --title "GROHBOT LIVE ' + str(tempf) + 'F - ' + str(humidity) + '%h" --top-banner --font "luxisr:15" static/grohbot.jpg'
	os.system(take_pic_command)


def all_off(devices):

	devices["lower_light"].state = 0
	devices["middle_light"].state = 0
	devices["top_fan"].state = 0
	devices["heater"].state = 0
	devices["internal_fan"].state = 0
	return devices


@app.route('/')
def index():

	imgstamp = time.time()
	temps, devices, configdata = page_stuff()

	action = request.args.get('action')

	if action == "alloff":
		devices = all_off(devices)

	if action == "lowerlighton":
		devices["lower_light"].state = 1

	if action == "lowerlightoff":
		devices["lower_light"].state = 0

	if action == "middlelighton":
		devices["middle_light"].state = 1

	if action == "middlelightoff":
		devices["middle_light"].state = 0

	if action == "heateron":
		devices["heater"].state = 1

	if action == "heateroff":
		devices["heater"].state = 0

	if action == "exhauston":
		devices["top_fan"].state = 1

	if action == "exhaustoff":
		devices["top_fan"].state = 1

	if action == "intakeon":
		devices["internal_fan"].state = 1

	if action == "intakeoff":
		devices["internal_fan"].state = 0

	save_device_states_to_file(devices)

	if action == "refresh":
		take_pic(temps.ftemp, temps.humidity)

	messagetext = "Catfish Clem has fallen down on the job. Again. We are sorry for his transgressions."
	return render_template('index.html', temps = temps, devices = devices, action = action, messagetext = messagetext, imgstamp = imgstamp, configdata = configdata)


@app.route('/mobile')
def mobile():

	temps, devices = page_stuff()

	return render_template('mobile.html', temps = temps)

if __name__ == '__main__':

 app.run(debug=True, host='10.0.0.199')
