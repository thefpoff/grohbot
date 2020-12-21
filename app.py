from flask import Flask, render_template
import time
import os
import datetime
import pickle
import csv
from TempHumMeasurements import TempHumMeasurements
from GrohbotConfig import GrohbotConfig

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

    os.system('tail -13 csv/dht.csv > csv/lastdht.csv')

    past_data = []

    with open('lastdht.csv', newline='') as csv_file:
    	reader = csv.reader(csv_file)
    	next(reader, None)  # Skip the header.
    	# Unpack the row directly in the head of the for loop.
    	for ftemp, humidity, lls, mls, efs, bfs, hs, datestamp in reader:
        	temps = TempHumMeasurements()
        	temps.ftemp = ftemp
        	temps.humidity = humidity
        	temps.time_taken = datestamp[0:5]
        	past_data.append(temps)

    past_data.reverse()

    return temps, devices, past_data

def take_pic(tempf, humidity):
	
	take_pic_command = 'fswebcam -r 640x480 -S 30 -F 10 --quiet --title "GROHBOT LIVE ' + str(tempf) + 'F - ' + str(humidity) + '%h" --top-banner --font "luxisr:15" static/grohbot.jpg'
	os.system(take_pic_command)


def test_all_off(devices):

	devices["lower_light"].state = 0
	devices["middle_light"].state = 0
	devices["top_fan"].state = 0
	devices["heater"].state = 0
	devices["internal_fan"].state = 0
	return devices

def lights_on(devices):

	devices["lower_light"].state = 1
	devices["middle_light"].state = 1
	devices["top_fan"].state = 0
	devices["heater"].state = 0
	devices["internal_fan"].state = 0
	return devices

@app.route('/')
def index():

	imgstamp = time.time()
	temps, devices, past_data = page_stuff()

	page = "HOME"
	messagetext = "Catfish Clem has fallen down on the job. Again."

	return render_template('index.html', temps = temps, devices = devices, page = page, past_data = past_data, messagetext = messagetext, imgstamp = imgstamp)


@app.route('/alloff')
def alloff():

	imgstamp = time.time()
	temps, devices, past_data = page_stuff()

	devices = test_all_off(devices)
	save_device_states_to_file(devices)

	page = "ALL OFF"
	messagetext = "ALL DEVICES TURNED OFF UNTIL NEXT LOGIC CYCLE"

	return render_template('index.html', temps = temps, devices = devices, page = page, past_data = past_data, messagetext = messagetext, imgstamp = imgstamp)

@app.route('/lowerlighton')
def lowerlighton():

	imgstamp = time.time()
	temps, devices, past_data = page_stuff()

	devices["lower_light"].state = 1
	
	save_device_states_to_file(devices)
	
	page = "LOWER LIGHTS ON"
	messagetext = "LOWER LIGHT ON UNTIL NEXT LOGIC CYCLE"

	return render_template('index.html', temps = temps, devices = devices, page = page, past_data = past_data, messagetext = messagetext, imgstamp = imgstamp)

@app.route('/lowerlightoff')
def lowerlightoff():

	imgstamp = time.time()
	temps, devices, past_data = page_stuff()

	devices["lower_light"].state = 0

	save_device_states_to_file(devices)
	
	page = "LOWER LIGHTS OFF"
	messagetext = "LOWER LIGHTS OFF UNTIL NEXT LOGIC CYCLE"

	return render_template('index.html', temps = temps, devices = devices, page = page, past_data = past_data, messagetext = messagetext, imgstamp = imgstamp)

@app.route('/middlelighton')
def middlelighton():

	imgstamp = time.time()
	temps, devices, past_data = page_stuff()
	
	devices["middle_light"].state = 1

	save_device_states_to_file(devices)
	
	page = "MIDDLE LIGHTS ON"
	messagetext = "MIDDLE LIGHTS ON UNTIL NEXT LOGIC CYCLE"

	return render_template('index.html', temps = temps, devices = devices, page = page, past_data = past_data, messagetext = messagetext, imgstamp = imgstamp)

@app.route('/middlelightoff')
def middlelightoff():

	imgstamp = time.time()
	temps, devices, past_data = page_stuff()
	
	devices["middle_light"].state = 0

	save_device_states_to_file(devices)
	
	page = "MIDDLE LIGHTS OFF"
	messagetext = "MIDDLE LIGHTS OFF UNTIL NEXT LOGIC CYCLE"

	return render_template('index.html', temps = temps, devices = devices, page = page, past_data = past_data, messagetext = messagetext, imgstamp = imgstamp)


@app.route('/heateron')
def heateron():

	imgstamp = time.time()
	temps, devices, past_data = page_stuff()

	devices["heater"].state = 1

	save_device_states_to_file(devices)
	
	page = "HEATER ON"
	messagetext = "HEATER ON UNTIL NEXT LOGIC CYCLE"

	return render_template('index.html', temps = temps, devices = devices, page = page, past_data = past_data, messagetext = messagetext, imgstamp = imgstamp)

@app.route('/heateroff')
def heateroff():

	imgstamp = time.time()
	temps, devices, past_data = page_stuff()

	devices["heater"].state = 0
	
	save_device_states_to_file(devices)
	
	page = "HEATER OFF"
	messagetext = "HEATER OFF UNTIL NEXT LOGIC CYCLE"

	return render_template('index.html', temps = temps, devices = devices, page = page, past_data = past_data, messagetext = messagetext, imgstamp = imgstamp)

@app.route('/exhauston')
def exhauston():

	imgstamp = time.time()
	temps, devices, past_data = page_stuff()

	devices["top_fan"].state = 1

	save_device_states_to_file(devices)
	
	page = "EXHAUST ON"
	messagetext = "EXHAUST ON UNTIL NEXT LOGIC CYCLE"

	return render_template('index.html', temps = temps, devices = devices, page = page, past_data = past_data, messagetext = messagetext, imgstamp = imgstamp)

@app.route('/exhaustoff')
def exhaustoff():

	imgstamp = time.time()
	temps, devices, past_data = page_stuff()

	devices["top_fan"].state = 0

	save_device_states_to_file(devices)
	
	page = "EXHAUST OFF"
	messagetext = "EXHAUST OFF UNTIL NEXT LOGIC CYCLE"

	return render_template('index.html', temps = temps, devices = devices, page = page, past_data = past_data, messagetext = messagetext, imgstamp = imgstamp)

@app.route('/intakeon')
def intakeon():

	imgstamp = time.time()
	temps, devices, past_data = page_stuff()

	devices["internal_fan"].state = 1

	save_device_states_to_file(devices)
	
	page = "INTAKE ON"
	messagetext = "INTAKE ON UNTIL NEXT LOGIC CYCLE"

	return render_template('index.html', temps = temps, devices = devices, page = page, past_data = past_data, messagetext = messagetext, imgstamp = imgstamp)

@app.route('/intakeoff')
def intakeoff():

	imgstamp = time.time()
	temps, devices, past_data = page_stuff()

	devices["internal_fan"].state = 0

	save_device_states_to_file(devices)
	
	page = "INTAKE OFF"
	messagetext = "INTAKE OFF UNTIL NEXT LOGIC CYCLE"

	return render_template('index.html', temps = temps, devices = devices, page = page, past_data = past_data, messagetext = messagetext, imgstamp = imgstamp)


@app.route('/imgrefresh')
def imgrefresh():

	imgstamp = time.time()
	temps, devices, past_data = page_stuff()

	take_pic(temps.ftemp, temps.humidity)

	page = "IMG REFRESH"
	messagetext = "IMAGE REFRESHED - CLICK HOME"

	return render_template('index.html', temps = temps, devices = devices, page = page, past_data = past_data, messagetext = messagetext, imgstamp = imgstamp)

@app.route('/mobile')
def mobile():

	temps, devices, past_data = page_stuff()

	return render_template('mobile.html', past_data = past_data, temps = temps)

if __name__ == '__main__':

 app.run(debug=True, host='10.0.0.199')
