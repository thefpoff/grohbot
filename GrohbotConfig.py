class GrohbotConfig():
	hour_lights_on = 20
	hour_lights_off = 14
	low_temp_trigger = 75
	high_temp_trigger = 90
	high_humid_trigger = 80

	mode = "Auto"

	write_to_csv_every_minutes = 10
	run_logic_every_minutes = 5
	take_pic_every_seconds = 20
	measure_th_every_seconds = 30
	set_states_from_pkl_every_seconds = 5

	req_sec_between_button_presses = .5
	check_mode_seconds = 1   # dont change this

	messagetext = "Has anyone seen Catfish Clem?"

	# working pins
	lower_light_pin = 20
	top_fan_pin = 6
	middle_light_pin = 13
	internal_fan_pin = 5
	heater_pin = 19
	dht_ground_relay_pin = 17

	dht22_pin = 10

	button_one_pin = 3
	button_two_pin = 2

	# not working yet pins
	bottom_fan_pin = 21
	top_light_pin = 0
	not_used_pin = 26
	

	
