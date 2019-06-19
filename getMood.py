'''
Uses Microsoft Azure API to read an image of a person's face and detect their emotions. Returns
a string containing the person's emotion. The four possible emotions it will return are "happy",
"sad", "relaxed", and "angry". If no face is detected in the image, the default return value is 
happy. The image that it tries to read in is called mood.jpg. 
'''

#Load libraries 
import requests
import json

#Main function for file, gets users mood based on picture
def getMood():
	subscription_key = 'f6116e88a1da406dbf18ed4a8c69f8c7'
	face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
	#image of person's face
	image_data = open('mood.jpg', 'rb').read()
	headers = { 'Ocp-Apim-Subscription-Key': subscription_key,
				'Content-Type': 'application/octet-stream' }
	params = { 'returnFaceId': 'false',
    		   'returnFaceLandmarks': 'false',
    		   'returnFaceAttributes': 'emotion' }

	#Uses Microsoft Azure API to read emotions from image of face
	response = requests.post(face_api_url, params=params, headers=headers, data=image_data)
	response = response.json()
	#If API could detect a face in the image, get microemotion amounts
	if response:
		#gets all microemotion amounts
		emotions = response[0]["faceAttributes"]["emotion"]
		anger = emotions["anger"]
		contempt = emotions["contempt"]
		disgust = emotions["disgust"]
		fear = emotions["fear"]
		happiness = emotions["happiness"]
		neutral = emotions["neutral"]
		sadness = emotions["sadness"]
		surprise = emotions["surprise"]
		#takes prevailing emotion from image
		emotion = max([anger, contempt, disgust, fear, happiness,
					   neutral, sadness, surprise])
		#returns one of four emotions based on emotions in datafile used for 
		#machine learning 
		if (emotion == anger or emotion == contempt or  emotion == disgust):
			return "angry"
		elif (emotion == fear or emotion == sadness):
			return "sad"
		elif (emotion == neutral):
			return "relaxed"
		else:
			return "happy"
	else:
		return "happy"
