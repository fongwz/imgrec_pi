from PIL import Image
import requests
import base64
import json

jpgfile = open("test3.jpg",'rb')
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