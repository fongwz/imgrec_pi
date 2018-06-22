from PIL import Image
import requests
import base64
import json
from picamera import PiCamera
from time import sleep

#"https://images.pexels.com/photos/415829/pexels-photo-415829.jpeg?auto=compress&cs=tinysrgb&h=350" sample url
def getBool(prompt):
	while True:
		try:
			return {"y":True, "n":False}[raw_input(prompt).lower()]
		except KeyError:
			print "Please input y/n only."

def createFace():
	print "------------Starting up camera--------------"
	camera = PiCamera()
	camera.start_preview()
	sleep(2)
	camera.capture('image.jpg')
	camera.stop_preview()
	print "------------Picture taken...----------------"

	#encoding the image
	jpgfile = open("image.jpg",'rb')
	jpgdata = jpgfile.read()
	b64_1 = base64.b64encode(jpgdata)


	url="https://api-us.faceplusplus.com/facepp/v3/detect"
	payload={
			'api_key':"_eLSJf561NiuuGdVKpahOF8soZpl7213"
			,'api_secret':"lQ6frS9V67fLRE1mJjskziK7pyoJC2gN"   
			,'image_base64': b64_1
			,'return_attributes':"gender,age,smiling,ethnicity"
			}
	response = requests.post(url, data=payload)
	print(response.status_code, response.reason)

	data = json.loads(response.text)
	print(data)
	print "---------------------------------------"
	if not data["faces"]:
		print("no faces found")
		return
	else:
		print("face detected")
		print("face token is %s" % data["faces"][0]["face_token"])
		token = data["faces"][0]["face_token"]

	print "---------------------------------------"
	print "Generating id for this image"
	name = raw_input("Enter name of person: ")

	#generate user-id for detected image
	url="https://api-us.faceplusplus.com/facepp/v3/face/setuserid"
	payload={
			'api_key':"_eLSJf561NiuuGdVKpahOF8soZpl7213"
			,'api_secret':"lQ6frS9V67fLRE1mJjskziK7pyoJC2gN"   
			,'face_token': token
			,'user_id': name
			}
	response = requests.post(url, data=payload)
	print(response.status_code, response.reason)
	data = json.loads(response.text)
	print(data)
	print("Token and id generated: %s ; %s" % (token,name))
	print "----------------------------------------"
	return token,name


def addToFaceSet(faceset_token, face_token):
	print "Now adding new face to faceset"
	url="https://api-us.faceplusplus.com/facepp/v3/faceset/addface"
	payload={
			'api_key':"_eLSJf561NiuuGdVKpahOF8soZpl7213"
			,'api_secret':"lQ6frS9V67fLRE1mJjskziK7pyoJC2gN"
			,'faceset_token':faceset_token
			,'face_tokens':face_token			
			}
	response = requests.post(url, data=payload)
	print(response.status_code, response.reason)
	print(json.loads(response.text))
	print "Successfully added face to faceset :)"
	return

def checkFaceExists(faceset_token, face_token):
	print "Checking if face exists in faceset.."
	url="https://api-us.faceplusplus.com/facepp/v3/search"
	payload={
			'api_key':"_eLSJf561NiuuGdVKpahOF8soZpl7213"
			,'api_secret':"lQ6frS9V67fLRE1mJjskziK7pyoJC2gN"
			,'face_token':face_token
			,'faceset_token':faceset_token			
			}
	response = requests.post(url, data=payload)
	print(response.status_code, response.reason)
	data = json.loads(response.text)
	print("threshold for user: %s is at: %f" % (data["results"][0]["user_id"], data["results"][0]["confidence"]))
	#set duplicate threshold to be 87%
	if (data["results"][0]["confidence"] > 87.0):
		print "There is already a person with a highly similar face in the faceset."
	else:
		print "Face does not exist in faceset"

	if getBool("Do you want to add this person into the faceset?(y/n) "):
		print "adding.."
		return True
	else:
		print "not adding..."
		return False
	return
#######################main program###########################

try:
	face_token,name = createFace()
	print "Successfully generated token and name :)"
	sleep(1)
except TypeError as err:
	print("Could not generate a token or name: {0}".format(err))
	sys.exit()
except:
	print "Unexpected error"

#get the faceset
url="https://api-us.faceplusplus.com/facepp/v3/faceset/getfacesets"
payload={
		'api_key':"_eLSJf561NiuuGdVKpahOF8soZpl7213"
		,'api_secret':"lQ6frS9V67fLRE1mJjskziK7pyoJC2gN"   
		}
response = requests.post(url, data=payload)
print(response.status_code, response.reason)

data = json.loads(response.text)
print("Obtained faceset token: %s" %data["facesets"][0]["faceset_token"])
faceset_token = data["facesets"][0]["faceset_token"]
sleep(1)

#check if face already exists in faceset(set minimum 87% confidence interval)
if checkFaceExists(faceset_token, face_token):
	print "Processing..."
	sleep(1)
	addToFaceSet(faceset_token, face_token)