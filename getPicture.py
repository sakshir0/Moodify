'''
Accesses a computer's webcam and takes a picture immediately. 
Saves picture to a file called mood.jpg in the same folder that
this Python file is contained in. 
'''

import cv2

def getPicture():
	camera = cv2.VideoCapture(0)
	return_value, image = camera.read()
	cv2.imwrite('mood'+'.jpg', image)
	del(camera)
