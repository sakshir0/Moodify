# Moodify

## Inspiration ##
The relationship between music and emotion is one that transcends most other sensory experiences. What people want to listen to at a given moment depends a lot on how they are currently feeling. Often, people want to listen to songs that are a certain “mood” that might not necessarily all be from the same genre to match how they are currently feeling. I wanted to create something for Spotify that would allow people to listen to music of a certain emotion. 

## What It Does ##
Moodify creates personalized Spotify playlists with up to 30 songs that fit the user’s current mood. It uses the five hundred most recent tracks saved to a user’s profile as possible songs for the playlist. There are four moods: happy, sad, angry, and relaxed. The mood of the user is obtained using either by taking a picture of the user’s face and reading their emotions or by them manually inputting a mood. 

## How It Works ##
The app uses a dataset from Last.fm that contains 2000 songs that have been manually tagged by users to be of a certain mood. It searches for these songs on Spotify and obtains their energy, valence, and “danceability”. I trained a Logistic Regression machine learning classifier to classify the songs into the different moods based on these audio features. I receive an accuracy rate on the validation data of about 80%.  The application accesses your personal Spotify account through the Spotify API and obtains your 500 most recent songs. It then classifies those songs into the four moods using the machine learning model and creates a playlist for you on Spotify with your songs in the mood you want.

## How To Use It ##
Download the source code and run the app through terminal with the command python spotify.py. The app will ask you for your Spotify user ID. If you created your account through Facebook, then go to your profile, click “Copy profile Link” and this will give you the unique ID connected with your account. 

## Built With ##
- [Spotify API](https://developer.spotify.com/documentation/web-api/)
- [Scikit-learn (sklearn)](https://scikit-learn.org/stable/documentation.html)
- [OpenCV](https://opencv.org/)
- [Microsoft Azure API](https://azure.microsoft.com/en-us/services/cognitive-services/face/)

## Video Demo ##
https://www.youtube.com/watch?v=Euq_iECaoW4
