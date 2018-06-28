from PIL import Image
import requests
import base64
import json
#from picamera import PiCamera
from time import sleep

#taking photo of user to process into api
#print "------------Starting up camera--------------"
#camera = PiCamera()
#camera.start_preview()
#sleep(2)
#camera.capture('image.jpg')
#camera.stop_preview()
#print "------------Picture taken...----------------"

#get faceset token first
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

#search faceset for highest compatibility face
jpgfile = open("./image.jpg",'rb')
jpgdata = jpgfile.read()
b64 = base64.b64encode(jpgdata)
print "Processing..."
sleep(1)

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
