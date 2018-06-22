import json
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import time
import threading


##########setup############
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(25, GPIO.IN)    # set GPIO 25 as input
flag = 0;
GPIO.add_event_detect(25, GPIO.RISING, callback=my_callback, bouncetime=200)
##########################3

def my_callback(channel):
	flag=1
	print "button pressed"

while(1):
	#do nothing