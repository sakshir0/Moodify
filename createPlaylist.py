'''
This file gets the 500 most recent tracks saved to a user's profile. 
It uses the already trained machine learning model and mood of the 
listener to create a new playlist with up to 30 songs that fit the user's 
current mood that is titled with the current mood. 
If a playlist with that name already already exists, a new playlist will 
be created and named "mood" 2. 
'''

#Load libraries
import getMood
import spotipy
import sys
import csv
import numpy as np
import time

'''
Takes in Spotify object and user ID and returns 
list of track URIs (strings) and list of names of the 
user's saved tracks (strings) in a tuple
'''
def getUserTracks(sp, user):
	results = []
	trackURIs = []
	tracks = []

	#total number of tracks to get
	numTracks = 500
	#max objects allowed for one API call
	maxObjects = 50
	#get numTracks most recent saved tracks from user
	for i in range(numTracks//maxObjects):
		savedTracks = sp.current_user_saved_tracks(limit=maxObjects, 
											  offset=i*maxObjects)
		if (savedTracks != None):
			results.append(savedTracks)
		'''
		results.append(sp.current_user_top_tracks(limit=maxObjects, 
												  offset=i*maxObjects))
		'''
	#analyze information about songs
	for item in results:
		for info in item['items']:
			'''
			trackURIs.append(info['uri'])
			tracks.append(info['name'] + " by " + info['artists'][0]['name'])
			'''
			trackURIs.append(info['track']['uri'])
			tracks.append(info['track']['name'] + " by " +
							   info['track']['artists'][0]['name'])
	return trackURIs, tracks

'''
Takes in list of track URIs and Spotify object
Returns 2D list of form [danceability, energy, valence] for each song
in list
'''
def getAudioFeatures(sp, trackURIs):
	features = []
	featuresTotal = []
	#max number of API calls
	max = 100
	for i in range(0, len(trackURIs), max):
		#get audio features of max tracks at once
		audioFeatures = sp.audio_features(trackURIs[i:i+max])
		#space time between API calls
		time.sleep(1)
		for j in range(len(audioFeatures)):
			if (audioFeatures != None):
				features.append(audioFeatures[j]['danceability'])
				features.append(audioFeatures[j]['energy'])
				features.append(audioFeatures[j]['valence'])
				featuresTotal.append(features)
			features = []
	return featuresTotal

'''
Takes in spotify object, user ID (string), list of user tracks URIs, 2D list of
features of the tracks in the form [[danceability, energy, valence]]
the string mood of the user, and the machine learning model.
Creates playlist for user based on their current mood and model out of 
their tracks. 
'''
def createPlaylist(sp, user, trackURIs, features, mood, model):
	featuresArray = np.asarray(features, dtype=np.float32)
	predictions = model.predict(featuresArray)
	songs = []
	playlistSongs = []

	#get all songs that match user's current mood and adds
	#up to 30 of them to playlist
	for i in range(len(predictions)):
		if (predictions[i] == mood):
			playlistSongs.append(trackURIs[i])
		if (len(playlistSongs) >= 30):
			break
	#create new playlist for user
	userID = user['id']
	playlist = sp.user_playlist_create(userID,name=mood,public=True)
	playlistID = playlist['id']
	#add songs to playlist
	sp.user_playlist_add_tracks(userID, playlistID, playlistSongs)

#main function for file, creates playlist
def main(sp, user, model, mood):
	trackURIs, tracks = getUserTracks(sp, user)
	features = getAudioFeatures(sp, trackURIs)
	createPlaylist(sp, user, trackURIs, features, mood, model)

