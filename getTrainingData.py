'''
This file uses the downloaded data called tagMoods.csv from Last.fm to create a training
set for Spotify moods. It searches Spotify for the track in the dataset
and if it is found, will record the danceability, energy, and valence of the track
along with the mood corresponding to the tags users marked on Last.fm. It will then
write the id of the track, the features, and the mood into a CSV file titled songMoods.csv.
This data will then be used to train the machine learning model.  
'''

#Load libraries
import pandas
import spotipy
import time
import csv

def searchForTracks(sp):
	# Load dataset from Last.fm
	dataset = pandas.read_csv("tagMoods.csv")
	#search spotify for the track, if found record uri and mood
	tracks = []
	tracksForData = []
	for i in range(len(dataset['title'])):
		title = dataset['title'][i]
		#searches for track from dataset in spotify to see if we can get features
		results = sp.search(q='track:' + title, type='track')
		#need to delay calls to API
		time.sleep(1)
		items = results['tracks']['items']
		#search found a track
		if (len(items) > 0):
			#checks if track has same artist as in dataset
			if (items[0]['artists'][0]['name'] == dataset['artist'][i]):
				tracks.append(items[0]['id'])
				tracksForData.append([items[0]['id'], dataset['mood'][i]])
	with open('tracksInSpotify.csv', mode='w') as file:
		writer = csv.writer(file, delimiter=',', 
	    				quotechar='"', 
	    				quoting=csv.QUOTE_MINIMAL)
	    #combine features and data into one line
		for i in range(len(tracksForData)):
			line = [tracksForData[i]]
			writer.writerow(line)

#returns 2D list of form [danceability, energy, valence] for each song
def getAudioFeatures(sp):
	#reads tracks found by spotify and reformats into 2D list
	dataset = pandas.read_csv("tracksInSpotify.csv")
	dataset = pandas.Series.tolist(dataset)
	tracks = []
	data = []
	for elem in dataset:
		res = elem[0].strip('][').replace("'", "").split(', ')
		data.append(res) 
		tracks.append(res[0])

	features = []
	featuresTotal = []
	#max number of API calls
	max = 100
	for i in range(0, len(tracks), max):
		#get audio features of max tracks at once
		audioFeatures = sp.audio_features(tracks[i:i+max])
		#space time between API calls
		time.sleep(1)
		for j in range(len(audioFeatures)):
			if (audioFeatures != None):
				features.append(audioFeatures[j]['danceability'])
				features.append(audioFeatures[j]['energy'])
				features.append(audioFeatures[j]['valence'])
				featuresTotal.append(features)
			features = []
	return data, featuresTotal

def writeToCSV(data, features):
	#write data to Excel file
	with open('songMoods.csv', mode='w') as file:
		writer = csv.writer(file, delimiter=',', 
	    				quotechar='"', 
	    				quoting=csv.QUOTE_MINIMAL)
	    #combine features and data into one line
		for i in range(len(features)):
			line = [data[i][0]] + features[i] + [data[i][1]]
			writer.writerow(line)

def main(sp):
	searchForTracks(sp)
	data, features = getAudioFeatures(sp)
	writeToCSV(data, features)