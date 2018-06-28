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

def clear_LED():
	GPIO.output(12, 0)
	GPIO.output(7, 0)

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

	retry = True;
	retryCount = 0;
	
	while retry and retryCount<10:
		url="https://api-us.faceplusplus.com/facepp/v3/detect"
		payload={
				'api_key':"_eLSJf561NiuuGdVKpahOF8soZpl7213"
				,'api_secret':"lQ6frS9V67fLRE1mJjskziK7pyoJC2gN"   
				,'image_base64': b64
				,'return_attributes':"facequality"
				}
		response = requests.post(url, data=payload)
		print(response.status_code, response.reason)
		if(response.status_code == 200):
			retryCount=0
			break
		else:
			retryCount+=1
			print("request failed, retrying %d out of 10 times" % retryCount)
		sleep(2)

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
	retry = True;
	retryCount = 0;
	while retry and retryCount < 10:
		print "getting faceset token..."
		url="https://api-us.faceplusplus.com/facepp/v3/faceset/getfacesets"
		payload={
				'api_key':"_eLSJf561NiuuGdVKpahOF8soZpl7213"
				,'api_secret':"lQ6frS9V67fLRE1mJjskziK7pyoJC2gN"   
				}
		response = requests.post(url, data=payload)
		print(response.status_code, response.reason)
		if(response.status_code == 200):
			retryCount=0
			break
		else:
			retryCount+=1
			print("request failed, retrying %d out of 10 times" % retryCount)
		sleep(2)
		
	data = json.loads(response.text)
	print("Faceset token is: %s" % data["facesets"][0]["faceset_token"])
	faceset_token = data["facesets"][0]["faceset_token"]
	print "---------------------------------------------"
	sleep(2) #prevent qps error

	print "now comparing..."
	retry = True;
	retryCount = 0;
	while retry and retryCount < 10:
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
		if(response.status_code == 200):
			retryCount=0
			break
		else:
			retryCount+=1
			print("request failed, retrying %d out of 10 times" % retryCount)
		sleep(2)

	try:
		data = json.loads(response.text)
		print(data)
		print "---------------------------------------------"
		if data["results"][0]["confidence"] > 87.0:
			print("Matched face with user_id: %s at confidence level: %f" % (data["results"][0]["user_id"], data["results"][0]["confidence"]))
			payload={
					'comparison_token':data["faces"][0]["face_token"],
					'comparison_image':b64,
					'user_id':data["results"][0]["user_id"],
					'face_token':data["results"][0]["face_token"],
					'confidence':data["results"][0]["confidence"]
			}
			url = "http://192.168.1.191:5000/compare"
			response = requests.post(url, data=payload)
			print(response.text)
			print(response.status_code, response.reason)
			GPIO.output(12, 1)
		else :
			print "no match for face in faceset"
			payload={
					'comparison_token':data["faces"][0]["face_token"],
					'comparison_image':b64,
					'user_id':data["results"][0]["user_id"],
					'face_token':data["results"][0]["face_token"],
					'confidence':data["results"][0]["confidence"]
			}
			url = "http://192.168.1.191:5000/compare"
			response = requests.post(url, data=payload)
			print(response.text)
			print(response.status_code, response.reason)
			GPIO.output(7, 1)
	except KeyError as err:
		print "max requests timeout error"
		sleep(2)

##########setup############
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(25, GPIO.IN)    # set GPIO 25 as input
GPIO.setup(12, GPIO.OUT, initial = 0)   # green led
GPIO.setup(7, GPIO.OUT, initial = 0)	# red led
GPIO.add_event_detect(25, GPIO.RISING, callback=my_callback, bouncetime=200)
camera = PiCamera()
###########################


#########main loop#########
try:
	while(1):
		if flag == 1:
			print "handled event"
			clear_LED()
			try:
				truefalse, b64 = check_quality()
				sleep(2) #prevent qps error
				compare_img(b64)
				sleep(2) #prevent qps error
			except TypeError as err:
				print("Did not pass quality check: {0}".format(err))
				GPIO.output(7, 1)
			flag = 0
			print "cleared flag"
except KeyboardInterrupt:
	GPIO.cleanup()
###########################