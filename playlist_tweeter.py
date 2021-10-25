# Author: Alphonso Bradham
# Date: Sep. 23 2020
# Purpose: A twitter bot {@SongsOfSolidarity} that posts a random communist song from
# any given youtube playlist


#TODO: Deploy to heroku and make sure there is some consistent output (once every 5 mins?)
#so that heroku doesnt shut program down.

#Document Imports:
import tweepy
import time
from googleapiclient.discovery import build
from random import randint

#Constants
YOUTUBE_API_KEY = '[INSERT YOUR KEY HERE]'
PLAYLIST_ID = '[PLAYLIST_ID HERE]'

TWITTER_API_KEY = '[INSERT YOUR KEY HERE]'
TWITTER_API_SECRET_KEY = '[INSERT YOUR KEY HERE]'

TWITTER_ACCESS_TOKEN = '1308913104684711948-vadRDKi8OlTsnH3Sm4fx3DoVeVJ9Vn'
TWITTER_ACCESS_TOKEN_SECRET = 'f6gqFmJKDRD3VFxUOvbkfEuJLqvdt0nAk3BHxZdbjovWl'

SLEEP_TIME = 28800 #8 Hours (measured in seconds)

#Building Youtube Services:
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

#Building/Authenticating Twitter Services:
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

twit_api = tweepy.API(auth)
try:
	twit_api.verify_credentials()
	print("Twitter Credential Verified")
except: 
	print("Error During Twitter Authentication")

#Functions

#Gets all video ids from the "Communist Songs playlist on youtube" and returns a list of id strings
def get_all_vids_in_playlist():

	video_ids = []
	next_page_token = None

	#Loop that executes so that we can get video ids from ALL PAGES of the playlist items array
	while True: 
		playlist_request = youtube.playlistItems().list(
			part = 'contentDetails',#Tells the api that we only want content details from each playlist item
			playlistId = COMMUNIST_SONGS_PLAYLIST_ID,
			maxResults = 50,
			pageToken = next_page_token #Keeps track of what the next page is (will break out of loop when this contains 'None')
			)

		#Makes http request and returns json
		playlist_response = playlist_request.execute()

		#Parses JSON response and save video ids in video_ids list
		for item in playlist_response['items']:
			playlist_item_video_id = item['contentDetails']['videoId']
			video_ids.append(playlist_item_video_id)

		#Get token for next page. If there is no next page, break out of the loop
		next_page_token = playlist_response.get('nextPageToken')
		if(next_page_token == None):
			break
	return video_ids

#Uses tweepy to post a tweet with the video link to the timeline
def make_tweet(youtube_url): 
	twit_api.update_status("https://www.youtube.com/watch?v=" + youtube_url)

#Program Start
def main():
	videos_to_tweet_from = get_all_vids_in_playlist()
	while(True):
		video_id_being_tweeted = videos_to_tweet_from[randint(0, 927)]
		make_tweet(video_id_being_tweeted)
		print("Tweeted video id: " + video_id_being_tweeted)
		time.sleep(SLEEP_TIME)



# Boilerplate / Start code. This project is intended to demonstrate the basic
# functionality of the twitter API.
if __name__ == '__main__':
	main()
