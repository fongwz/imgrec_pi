from PIL import Image
import requests
import base64
import json

jpgfile = open("./faces/1.jpg",'rb')
jpgdata = jpgfile.read()
b64 = base64.b64encode(jpgdata)

#url="https://api-us.faceplusplus.com/facepp/v3/detect"
payload={
		'api_key':"_eLSJf561NiuuGdVKpahOF8soZpl7213"
		,'api_secret':"lQ6frS9V67fLRE1mJjskziK7pyoJC2gN"   
		,'image_base64': "omega"
		,'return_attributes':"facequality"
		}





print "------------------------------------"

#Sending data to backend to update db
url = "http://192.168.1.191:5000/create"
response = requests.post(url,
headers = { 'Content-type': 'application/json'},
data = json.dumps({
	'Description':'Information',
	'Keywords':'Information',
    'name': 'asd',
    'face_token': 'bss',
    'body': b64
    })
) 
print response.text