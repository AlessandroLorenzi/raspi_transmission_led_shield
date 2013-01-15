#!/usr/bin/python
# -*- coding: utf-8 -*- 
import RPi.GPIO as GPIO, time
import transmissionrpc
import subprocess

def transmission_is_up():
	try:
		server = transmissionrpc.Client("localhost")
	except:
		GPIO.output(18, False)  
		GPIO.output(22, False)  
		GPIO.output(23, False)  
		GPIO.output(24, True) 
		return False
	
	GPIO.output(24, False) 
	return True

def check_download():

	downloading = 0
	seeding = 0

	server = transmissionrpc.Client("localhost")
	for torrent in server.list():
		if server.list()[torrent].status == "downloading":
			downloading += 1
		if server.list()[torrent].status == "seeding":
			seeding += 1
	if downloading > 0:
		GPIO.output(23, True)  
	else:
		GPIO.output(23, False)  
	
	if seeding > 0:
		GPIO.output(18, True)  
	else:
		GPIO.output(18, False)  
		

def transmission_on_off(oldstatus):
	# Read if button is not pressed. 
	# i wonder why if not pressed return value is a random value (true/false)
	# while if is pressed is true

	count = 0
	while count < 5000:
		if GPIO.input(25) == True:
			return False
		count +=1
	
	if oldstatus==True:
		return True
	print("button")

	status = transmission_is_up()
	GPIO.output(18, True)  
	GPIO.output(23, True)  
	GPIO.output(24, True) 

	if status:
		subprocess.Popen("killall transmission-daemon", shell=True)
		subprocess.Popen("umount /home/alorenzi/Transmission", shell=True)
	else:
		subprocess.Popen("mount -L transmission ", shell=True)
		subprocess.Popen("su alorenzi -c transmission-daemon", shell=True)
	
	return True

def modify_alt_speed(alt_speed_pressed, alt_speed):
	# Read if alt speed button is pressed. 
	# i wonder why if not pressed return value is a random value (true/false)
	# while if is pressed is true

	count = 0
	while count < 5000:
		if GPIO.input(17) == True:
			return (False, alt_speed)
		count +=1
	
	
	if alt_speed_pressed==True:
		return (True, alt_speed)



	if alt_speed:
		#  set alt_speed off
		subprocess.Popen("transmission-remote localhost --no-alt-speed", shell=True)
		GPIO.output(22, False)  
		return(True, False)
	else:
		# set alt_speed on
		subprocess.Popen("transmission-remote localhost --alt-speed", shell=True)
		GPIO.output(22, True)  
		return(True, True)

	

# Port description:
# 18: green led
# 17: alternate speed button
# 22: alternate speed led
# 23: yellow led
# 24: red led
# 25: on/off button
	
# Setup GPIO
GPIO.setmode(GPIO.BCM)  
GPIO.setup(18, GPIO.OUT)
GPIO.setup(17, GPIO.IN) 
GPIO.setup(22, GPIO.OUT) 
GPIO.setup(23, GPIO.OUT) 
GPIO.setup(24, GPIO.OUT) 
GPIO.setup(25, GPIO.IN)

r = 0


oldstatus = False
alt_speed = False
alt_speed_pressed = False
while 1:
	if r == 0:
		r = 1000
		if transmission_is_up():
			check_download()
	r -= 1
	
	oldstatus=transmission_on_off(oldstatus)

	(alt_speed_pressed, alt_speed) = modify_alt_speed(alt_speed_pressed, alt_speed)
	
	if oldstatus:
		time.sleep(1)
		r = 0

	time.sleep(0.1)


