from PIL import Image
import requests
import base64
import json
from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.start_preview()
sleep(2)
camera.capture('image.jpg')
camera.stop_preview()

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
jpgfile = open("image.jpg",'rb')
jpgdata = jpgfile.read()
b64 = base64.b64encode(jpgdata)

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

