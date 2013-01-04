# -*- coding: utf-8 -*- 
import RPi.GPIO as GPIO, time
import transmissionrpc

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
	server = transmissionrpc.Client("localhost")
	downloading = 0
	seeding = 0
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
		

		
	

GPIO.setmode(GPIO.BCM)  
GPIO.setup(18, GPIO.OUT) # definiamo che il la GPIO18 (pin12) è un uscita
GPIO.setup(23, GPIO.OUT) # definiamo che il la GPIO18 (pin12) è un uscita
GPIO.setup(24, GPIO.OUT) # definiamo che il la GPIO18 (pin12) è un uscita

while 1:
	if transmission_is_up():
		check_download()

	time.sleep(1)


def round(): 
	GPIO.output(24, False)  # GPIO a 1 (HIGH), led accesso
	GPIO.output(18, True)  # GPIO a 1 (HIGH), led accesso
	time.sleep(1)          # attendi 1 secondo
	GPIO.output(18, False) # GPIO a 0 (LOW), led spento
	GPIO.output(23, True)  # GPIO a 1 (HIGH), led accesso
	time.sleep(1)          # attendi 1 secondo e ricomincia
	GPIO.output(23, False)  # GPIO a 1 (HIGH), led accesso
	GPIO.output(24, True)  # GPIO a 1 (HIGH), led accesso
	time.sleep(1)          # attendi 1 secondo
