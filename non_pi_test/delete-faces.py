from PIL import Image
import requests
import base64
import json

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

print "---Now getting details of faceset---"
url="https://api-us.faceplusplus.com/facepp/v3/faceset/removeface"
payload={
		'api_key':"_eLSJf561NiuuGdVKpahOF8soZpl7213"
		,'api_secret':"lQ6frS9V67fLRE1mJjskziK7pyoJC2gN"
		,'faceset_token':faceset_token
		,'face_tokens':"11621aaf067e702fc543e22be560a53a,3d193acdaf34d629216d4a1d18892dd1,3f068ffc6eb1e75d5aba341c3da19b3c,17967f1fed97b78a189c294dd7a48f91"	
		}
response = requests.post(url, data=payload)
print(response.status_code, response.reason)
print(json.dumps(json.loads(response.text)))