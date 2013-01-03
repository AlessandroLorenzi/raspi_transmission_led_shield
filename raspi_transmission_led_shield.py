# -*- coding: utf-8 -*- 
import RPi.GPIO as GPIO, time
import subprocess

def transmission_is_up():
	p = subprocess.Popen("/usr/bin/ps aux| grep transmission-daemon | grep -v grep | wc -l", stdout=subprocess.PIPE ,shell=True)
	out =  int(p.stdout.read())
	if out == 1:
	        GPIO.output(24, False) 
                check_download()

	else:
	        GPIO.output(18, False)  
	        GPIO.output(23, False)  
	        GPIO.output(24, True) 

def check_download():
	p = subprocess.Popen("transmission-remote localhost  --list | wc -l", stdout=subprocess.PIPE ,shell=True)
	active =  int(p.stdout.read())-2

	p = subprocess.Popen("transmission-remote localhost  --list |grep \"100%\" |  wc -l", stdout=subprocess.PIPE ,shell=True)
	done =  int(p.stdout.read())-2
	if active > 0:
		GPIO.output(23, True)  
	else:
		GPIO.output(23, False)  
	
	if done > 0:
		GPIO.output(24, True)  
	else:
		GPIO.output(24, False)  
		

		
	

GPIO.setmode(GPIO.BCM)  
GPIO.setup(18, GPIO.OUT) # definiamo che il la GPIO18 (pin12) è un uscita
GPIO.setup(23, GPIO.OUT) # definiamo che il la GPIO18 (pin12) è un uscita
GPIO.setup(24, GPIO.OUT) # definiamo che il la GPIO18 (pin12) è un uscita

while 1:
	transmission_is_up()
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
