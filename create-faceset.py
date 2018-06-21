from PIL import Image
import requests
import base64
import json

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


#search faceset for highest confidence image
url="https://api-us.faceplusplus.com/facepp/v3/search"
payload={
		'api_key':"_eLSJf561NiuuGdVKpahOF8soZpl7213"
		,'api_secret':"lQ6frS9V67fLRE1mJjskziK7pyoJC2gN"   
		,'display_name': "test_1"
		}
response = requests.post(url, data=payload)
print(response.status_code, response.reason)

data = json.loads(response.text)