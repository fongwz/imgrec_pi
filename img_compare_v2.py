import RPi.GPIO as GPIO
import time
import threading
from PIL import Image
import requests
import base64
import json
from picamera import PiCamera
from time import sleep


################global variables#################
flag = 0;
#################################################


def my_callback(channel):
	global flag
	if flag == 0:
		flag=1
	print "button pressed"

def check_quality():
	#taking photo of user to process into api
	print "------------Starting up camera--------------"
	camera.start_preview()
	sleep(5)
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
	#print(data["faces"][0]["attributes"]["facequality"]["value"])
	#print(data["faces"][0]["attributes"]["facequality"]["threshold"])
	print "---------------------------------------"
	try:
		if not data["faces"]:
			print "no faces found"
			return False
		elif data["faces"][0]["attributes"]["facequality"]["value"] < data["faces"][0]["attributes"]["facequality"]["threshold"]:
			print "picture quality fell below threshold"
			return False
		else :
			print "quality check passed"
			return True, b64
	except KeyError as err:
		print("something went wrong..:%s" % format(err))
		return False

def compare_img(b64):
	#get faceset token first
	print "getting faceset token..."
	url="https://api-us.faceplusplus.com/facepp/v3/faceset/getfacesets"
	payload={
			'api_key':"_eLSJf561NiuuGdVKpahOF8soZpl7213"
			,'api_secret':"lQ6frS9V67fLRE1mJjskziK7pyoJC2gN"   
			}
	response = requests.post(url, data=payload)
	print(response.status_code, response.reason)
	data = json.loads(response.text)
	print("Faceset token is: %s" % data["facesets"][0]["faceset_token"])
	faceset_token = data["facesets"][0]["faceset_token"]
	print "---------------------------------------------"
	sleep(2) #prevent qps error

	print "now comparing..."
	retry = True;
	while retry:
		try:
			url="https://api-us.faceplusplus.com/facepp/v3/search"
			payload={
					'api_key':"_eLSJf561NiuuGdVKpahOF8soZpl7213"
					,'api_secret':"lQ6frS9V67fLRE1mJjskziK7pyoJC2gN"   
					,'image_base64': b64
					,'faceset_token': faceset_token
					,'return_result_count': 5	
					}
			response = requests.post(url, data=payload)
			print(response.status_code, response.reason)
			data = json.loads(response.text)
			print(data)
			print "---------------------------------------------"
			if data["results"][0]["confidence"] > 87.0:
				print("Matched face with user_id: %s at confidence level: %f" % (data["results"][0]["user_id"], data["results"][0]["confidence"]))
				GPIO.output(12, 1)
			else :
				print "no match for face in faceset"
			retry = False;
		except KeyError as err:
			print "Concurrency limit occurred, trying again after sleeping for 2s..."
			retry = True;
			sleep(2)

##########setup############
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(25, GPIO.IN)    # set GPIO 25 as input
GPIO.setup(12, GPIO.OUT)   # set GPIO 12 as output
GPIO.add_event_detect(25, GPIO.RISING, callback=my_callback, bouncetime=200)
camera = PiCamera()
###########################


#########main loop#########
try:
	while(1):
		if flag == 1:
			print "handled event"
			GPIO.output(12, 0)
			try:
				truefalse, b64 = check_quality()
				sleep(2) #prevent qps error
				compare_img(b64)
				sleep(2) #prevent qps error
			except TypeError as err:
				print("Did not pass quality check: {0}".format(err))
			
			flag = 0
			print "cleared flag"
except KeyboardInterrupt:
	GPIO.cleanup()
###########################