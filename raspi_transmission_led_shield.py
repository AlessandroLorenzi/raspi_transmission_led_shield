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

	status = transmission_is_up()
	GPIO.output(18, True)  
	GPIO.output(23, True)  
	GPIO.output(24, True) 
	print "slipping"

	if status:
		print ("killing transmission")
		subprocess.Popen("killall transmission-daemon", shell=True)
		subprocess.Popen("umount /home/alorenzi/Transmission", shell=True)
	else:
		print ("starting transmission")
		subprocess.Popen("mount -L transmission ", shell=True)
		subprocess.Popen("su alorenzi -c transmission-daemon", shell=True)
	
	return True

	

GPIO.setmode(GPIO.BCM)  
GPIO.setup(18, GPIO.OUT) # definiamo che il la GPIO18 (pin12) è un uscita
GPIO.setup(23, GPIO.OUT) # definiamo che il la GPIO18 (pin12) è un uscita
GPIO.setup(24, GPIO.OUT) # definiamo che il la GPIO18 (pin12) è un uscita
GPIO.setup(25, GPIO.IN) # definiamo che il GPIO17 è un ingresso

r = 0


oldstatus = False
while 1:
	if r == 0:
		r = 1000
		if transmission_is_up():
			check_download()
	r -= 1
	
	oldstatus=transmission_on_off(oldstatus)
	
	if oldstatus:
		time.sleep(1)
		r = 0

	time.sleep(0.1)


