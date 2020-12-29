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

def get_temps_and_devices():

	# open the file where data is dumped
	fileo = open('pickles/temphum.pkl', 'rb')
	temps = pickle.load(fileo)
	fileo.close()

	# open the file where data is dumped
	fileo = open('pickles/devices_states.pkl', 'rb')
	devices = pickle.load(fileo)
	fileo.close()
	
	
	return temps, devices

def take_pic(tempf, humidity):
	
	take_pic_command = 'fswebcam -r 640x480 -S 30 -F 10 --quiet --banner-colour "#ffa50096" --line-colour "#ffa500" --title "GROHBOT LIVE ' + str(tempf) + 'F - ' + str(humidity) + '%H" --top-banner --font "luxisr:15" static/grohbot.jpg'
	os.system(take_pic_command)


@app.route('/')
def index():

	temps, devices = get_temps_and_devices()
	configdata = get_config_from_file()

	action = request.args.get('action')

	if action == "lowerlighton":
		devices["lower_light"].state = 1
		save_device_states_to_file(devices)

	if action == "lowerlightoff":
		devices["lower_light"].state = 0
		save_device_states_to_file(devices)

	if action == "middlelighton":
		devices["middle_light"].state = 1
		save_device_states_to_file(devices)

	if action == "middlelightoff":
		devices["middle_light"].state = 0
		save_device_states_to_file(devices)

	if action == "heateron":
		devices["heater"].state = 1
		save_device_states_to_file(devices)

	if action == "heateroff":
		devices["heater"].state = 0
		save_device_states_to_file(devices)

	if action == "exhauston":
		devices["top_fan"].state = 1
		save_device_states_to_file(devices)

	if action == "exhaustoff":
		devices["top_fan"].state = 1
		save_device_states_to_file(devices)

	if action == "intakeon":
		devices["internal_fan"].state = 1
		save_device_states_to_file(devices)

	if action == "intakeoff":
		devices["internal_fan"].state = 0
		save_device_states_to_file(devices)


	if action == "refresh":
		take_pic(temps.ftemp, temps.humidity)
	
	
	if action == "Auto":
		# set mode to "Auto"
		configdata = get_config_from_file()
		configdata.mode = "Auto"
		configdata.messagetext = "LOGIC MODE ACTIVE"
		save_config_to_file(configdata)

	if action == "Manual":
		# set mode to "Manual"
		configdata = get_config_from_file()
		configdata.mode = "Manual"
		configdata.messagetext = "MANUAL MODE ACTIVE - logic will NOT run"
		save_config_to_file(configdata)

	if request.args.get('hour_lights_on', type=int): 
		configdata = get_config_from_file()
		configdata.hour_lights_on = request.args.get('hour_lights_on', type=int)
		configdata.hour_lights_off = request.args.get('hour_lights_off', type=int)
		configdata.low_temp_trigger = request.args.get('low_temp_trigger', type=int)
		configdata.high_temp_trigger = request.args.get('high_temp_trigger', type=int)
		configdata.high_humid_trigger = request.args.get('high_humid_trigger', type=int)

		save_config_to_file(configdata)

		configdata.messagetext = "saved new config to file"

	imgstamp = time.time()

	return render_template('index.html', temps = temps, devices = devices, action = action, imgstamp = imgstamp, configdata = configdata)


@app.route('/mobile')
def mobile():

	temps, devices = page_stuff()

	return render_template('mobile.html', temps = temps)

if __name__ == '__main__':

 app.run(debug=True, host='10.0.0.199')
