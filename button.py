import json
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import time
import threading

flag = 0;

def my_callback(channel):
	global flag
	if flag == 0:
		flag=1
	print "button pressed"

def check_quality():
	#taking photo of user to process into api
	print "------------Starting up camera--------------"
	camera = PiCamera()
	camera.start_preview()
	sleep(2)
	camera.capture('image.jpg')
	camera.stop_preview()
	print "------------Picture taken...----------------"

	jpgfile = open("image.jpg",'rb')
	jpgdata = jpgfile.read()
	b64 = base64.b64encode(jpgdata)

	url="https://api-us.faceplusplus.com/facepp/v3/detect"
	payload={
			'api_key':"_eLSJf561NiuuGdVKpahOF8soZpl7213"
			,'api_secret':"lQ6frS9V67fLRE1mJjskziK7pyoJC2gN"   
			,'image_base64': b64
			,'return_attributes':"facequality"
			}
	response = requests.post(url, data=payload)
	print(response.status_code, response.reason)

	data = json.loads(response.text)
	print(data)
	print "---------------------------------------"
	if not data["faces"]:
		print("no faces found")
	else :
		print

##########setup############
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(25, GPIO.IN)    # set GPIO 25 as input
GPIO.add_event_detect(25, GPIO.RISING, callback=my_callback, bouncetime=200)
##########################3


while(1):
	if flag == 1:
		print "handled event"
		check_quality()
		flag = 0
