#!/usr/bin/python

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import wiringpi 
import adafruit_dht

import time
import os
import os.path
from os import path
import datetime
import pickle
import csv

from RepeatedTimer import RepeatedTimer
from Device import Device
from TempHumMeasurements import TempHumMeasurements
from GrohbotConfig import GrohbotConfig
#from Sheets_Logging import Sheets_Logging

 
wiringpi.wiringPiSetup() 
serial = wiringpi.serialOpen('/dev/ttyS0',9600) 

##############################
#       PINS        

# working pins
lower_light_pin = 20
top_fan_pin = 6
middle_light_pin = 13
internal_fan_pin = 5
heater_pin = 19

dht22_pin = 10

button_one_pin = 3
button_two_pin = 2

# not working yet pins
bottom_fan_pin = 21
top_light_pin = 0
ceiling_light_pin = 26



#    END PINS   
###########################


lower_light = Device()
lower_light.name = "Lower Light"
lower_light.state = 0 
lower_light.pin = lower_light_pin
lower_light.page = "lowerlight"

middle_light = Device()
middle_light.name = "Middle Light"
middle_light.state = 0
middle_light.pin = middle_light_pin
middle_light.page = "middlelight"

top_fan = Device()
top_fan.name = "Exhaust Fan"
top_fan.state = 0 
top_fan.pin = top_fan_pin
top_fan.page = "exhaust"

internal_fan = Device()
internal_fan.name = "Breeze Fan"
internal_fan.state = 0
internal_fan.pin = internal_fan_pin
internal_fan.page = "intake"

heater = Device()
heater.name = "Heater"
heater.state = 0
heater.pin = heater_pin
heater.page = "heater"

devices = {'lower_light':lower_light, 'middle_light':middle_light,  'top_fan':top_fan,  'internal_fan':internal_fan, 'heater':heater}   
device_names = ['lower_light', 'middle_light', 'top_fan', 'internal_fan', 'heater']
device_count = 0

# set up configuration
grohbotconfig = GrohbotConfig()

last_button_press_time = time.time()
req_sec_between_button_presses = .5

check_mode_seconds = 1

last_run_minute = datetime.datetime.now().minute
last_run_second = datetime.datetime.now().second


def print_lcd_line_0(text):
    wiringpi.serialPuts(serial,'?f') #clear screen line one
    wiringpi.serialPuts(serial, text)

    #print("lcd0:" + text)

def print_lcd_line_1(text):
    wiringpi.serialPuts(serial,'?x00?y1') #set cursor to second line
    wiringpi.serialPuts(serial, text)

    #print("lcd1:" + text)


def change_device_state(device):

    global devices

    if device.state == 1:
        device.state = 0    
        GPIO.output(device.pin, GPIO.HIGH)
        
    else:
        device.state = 1
        GPIO.output(device.pin, GPIO.LOW)
    
    save_device_states_to_file(devices)                    

def device_state_on(device):

    global devices

    GPIO.output(device.pin, GPIO.LOW)
    save_device_states_to_file(devices)


def device_state_off(device):

    global devices

    GPIO.output(device.pin, GPIO.HIGH)
    save_device_states_to_file(devices)


def accept_button_press(button_press_time):

    global last_button_press_time

    time_passed =  button_press_time - last_button_press_time
    
    if time_passed > req_sec_between_button_presses:
        last_button_press_time = button_press_time
        return True 

    else:
        return False 



def button_callback_one(channel):

    global device_count
    
    if accept_button_press(time.time()):
        print("------>  ONE")
        device_count = device_count + 1
        if device_count > len(devices)-1:
                device_count = 0 

        current_device = devices[device_names[device_count]]
        device_state = current_device.state
        device_state_name = current_device.state_options[device_state]
        print_lcd_line_0(current_device.name)
        print_lcd_line_1(device_state_name)

    

def button_callback_two(channel):

    global device_count 


    if accept_button_press(time.time()):
        print("-------------->  TWO")
        current_device = devices[device_names[device_count]]

        change_device_state(current_device)

        device_state = current_device.state
        device_state_name = current_device.state_options[device_state]
        print_lcd_line_0(current_device.name)
        print_lcd_line_1(device_state_name)
     
    

def get_temp():

    try:
        temperature_c = round(dhtDevice.temperature, 2)
        temperature_f = round(temperature_c * (9 / 5) + 32, 2)
        humidity = round(dhtDevice.humidity, 2)
    
        return temperature_f, humidity

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print("TRYNUM: " + str(i) + error.args[0])
        #return "ERR", "ERR"
    
    except Exception as error:
        dhtDevice.exit()
        print("DHT CHECK EXCEPTION ################################")
        raise error   

def set_device_state_relays(devices):

    global last_button_press_time

    # fake button press to keep buttons from firing unwanted
    last_button_press_time = time.time()
 
    for i in devices:
        if devices[i].state == 1:
            device_state_on(devices[i])
        else:
            device_state_off(devices[i])

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

def save_device_states_to_file(devices):

    # file for saving/pickle 
    file = open('pickles/devices_states.pkl', 'wb')
    pickle.dump(devices, file)
    file.close()


def get_device_states_from_file():

    # open the file where data is dumped
    fileo = open('pickles/devices_states.pkl', 'rb')
    datao = pickle.load(fileo)
    fileo.close()

    return datao

def print_device_states(devices):
    
    print("GROHBOT STATUS:")

    for i in devices:
        print(devices[i].name + " : " + str(devices[i].state))

    # Path
    path = 'pickles/devices_states.pkl'

    # Get the time of last modifation of the specified path since the epoch
    modification_time = os.path.getmtime(path)
    # convert the time in seconds since epoch to local time
    local_time = time.ctime(modification_time)
    print( local_time )

def save_data_to_csv(ftemp, humidity, devices):

    # save data to csv file 
    data_row = [ftemp, humidity, devices["lower_light"].state, devices["middle_light"].state, devices["top_fan"].state, devices["internal_fan"].state, devices["heater"].state, time.strftime('%X %x %Z')]
    save_row_to_csv(data_row)


def save_row_to_csv(data_row):

    if path.exists("static/csv/dht.csv"):
        # file exists, write row
        with open('static/csv/dht.csv', 'a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
            csv_writer.writerow(data_row)

    else:
        # file doesn't exist, create and write header
        data_row = ["Temp", "Humidity", "Lower Light State", "Middle Light State", "Exhaust Fan State", "Breeze Fan State", "Heater State", "Datetime"]
        with open('static/csv/dht.csv', 'a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
            csv_writer.writerow(data_row)
            
    # create file for graph on webpage
    os.system('head -n 1 static/csv/dht.csv > static/csv/lastdht.csv')
    os.system('tail -n 20 static/csv/dht.csv >> static/csv/lastdht.csv')

def save_temps_to_file(ftemp, humidity):

    temps = TempHumMeasurements()
    temps.ftemp = ftemp
    temps.humidity = humidity

    # file for saving/pickle 
    file = open('pickles/temphum.pkl', 'wb')
    pickle.dump(temps, file)
    file.close()

def get_temps_from_file():

    # open the file where data is dumped
    fileo = open('pickles/temphum.pkl', 'rb')
    temps = pickle.load(fileo)
    fileo.close()

    return temps.ftemp, temps.humidity

def take_pic(tempf, humidity):
    
    take_pic_command = 'fswebcam -r 640x480 -S 30 -F 10 --quiet --title "GROHBOT LIVE ' + str(tempf) + 'F - ' + str(humidity) + '%h" --top-banner --font "luxisr:15" static/grohbot.jpg'
    os.system(take_pic_command)


def set_states_by_logic(ftemp, humidity, devices):

    config = get_config_from_file()
    
    localtime = time.localtime(time.time())
 
    print_lcd_line_0(time.strftime("%m/%d, %H:%M:%S", time.localtime()))
    
    if localtime.tm_hour >= config.hour_lights_on or localtime.tm_hour < config.hour_lights_off:

        print_lcd_line_1("LT: " + str(ftemp) + "f " + str(humidity) + "H")
        devices["lower_light"].state = 1
        devices["middle_light"].state = 1

    else: 
        print_lcd_line_1("NT: " + str(ftemp) + "f " + str(humidity) + "H")
        devices["lower_light"].state = 0
        devices["middle_light"].state = 0
    

    if ftemp != "ERR":   

        if ftemp > config.high_temp_trigger:
            devices["top_fan"].state = 1
        else:
            devices["top_fan"].state = 0

        if ftemp < config.low_temp_trigger:
            devices["heater"].state = 1
            devices["internal_fan"].state = 1
        else: 
            devices["heater"].state = 0
            devices["internal_fan"].state = 0
            devices["top_fan"].state = 0

    if humidity != "ERR":

        if humidity > config.high_humid_trigger:
            devices["top_fan"].state = 1
        else:
            devices["top_fan"].state = 0

    return devices

def time_to_run_minutes(devisor):

    current_minutes = datetime.datetime.now().minute
    remainder = current_minutes % devisor 

    if remainder == 0:
        return True 
    else:
        return False 

def time_to_run_seconds(devisor):

    current_seconds = datetime.datetime.now().second
    remainder = current_seconds % devisor 

    if remainder == 0:
        return True 
    else:
        return False 


def tick_tock():
    
    global devices
    global last_run_minute
    global last_run_second

    if last_run_minute != datetime.datetime.now().minute:

        #haven't run yet this minute 
        #set last_run_minute so we don't run again this minute
        last_run_minute = datetime.datetime.now().minute

        if time_to_run_minutes(5): # Do this every n minutes

            ftemp, humidity = get_temps_from_file()
            devices = set_states_by_logic(ftemp, humidity, devices)
            save_device_states_to_file(devices) 
            print_device_states(devices)
            print("RAN LOGIC")


        if time_to_run_minutes(10):
        
            ftemp, humidity = get_temps_from_file()
            save_data_to_csv(ftemp, humidity, devices)
            print("WROTE TO CSV FILE")  

    if last_run_second != datetime.datetime.now().second:

        # we haven't run this second before 
        # set so we don' run again this second 
        last_run_second = datetime.datetime.now().second

        if time_to_run_seconds(5): # Do this every n seconds

                devices = get_device_states_from_file()
                set_device_state_relays(devices)


                print_lcd_line_0(time.strftime("%m/%d, %H:%M:%S", time.localtime()))
                ftemp, humidity = get_temps_from_file()
                print_lcd_line_1("NOW:" + str(ftemp) + "F " + str(humidity) + "H")
                print("SET STATE FROM PKL")

        if time_to_run_seconds(30): 

                ftemp, humidity = get_temp()
                save_temps_to_file(ftemp, humidity)
                print("HT MEASUREMENT: " + str(ftemp) + "F " + str(humidity) + "%H")

                take_pic(ftemp, humidity)
                print("TOOK PICTURE")

    

#GPIO.setwarnings(False) # Ignore warning for now
#GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

# Set button pins to be an input pin and set initial value to be pulled low (off)
GPIO.setup(button_one_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(button_two_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.add_event_detect(button_one_pin, GPIO.RISING,callback=button_callback_one, bouncetime=300)
GPIO.add_event_detect(button_two_pin, GPIO.RISING,callback=button_callback_two, bouncetime=300) 

# set up working pins and turn them all off at startup 
GPIO.setup(lower_light_pin, GPIO.OUT)
GPIO.output(lower_light_pin, GPIO.HIGH)
GPIO.setup(middle_light_pin, GPIO.OUT)
GPIO.output(middle_light_pin, GPIO.HIGH)
GPIO.setup(top_fan_pin, GPIO.OUT)
GPIO.output(top_fan_pin, GPIO.HIGH)
GPIO.setup(internal_fan_pin, GPIO.OUT)
GPIO.output(internal_fan_pin, GPIO.HIGH)
GPIO.setup(heater_pin, GPIO.OUT)
GPIO.output(heater_pin, GPIO.HIGH)

# pins not being used, still turning them off at startup 
GPIO.setup(bottom_fan_pin, GPIO.OUT)
GPIO.output(bottom_fan_pin, GPIO.HIGH)
GPIO.setup(top_light_pin, GPIO.OUT)
GPIO.output(top_light_pin, GPIO.HIGH)
GPIO.setup(ceiling_light_pin, GPIO.OUT)
GPIO.output(ceiling_light_pin, GPIO.HIGH)

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(dht22_pin)

save_config_to_file(grohbotconfig)
save_device_states_to_file(devices)
save_temps_to_file(70, 30)

timer = RepeatedTimer(check_mode_seconds, tick_tock)

print_lcd_line_0("GROHBOT ACTIVE") 

message = input("Press enter to quit\n") # Run until someone presses enter
print("QUITTING")
GPIO.cleanup() # Clean up
timer.stop() # stop timer 
