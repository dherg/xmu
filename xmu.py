
# xmu playlist URI: spotify:user:spotyams:playlist:6HxlZvtJfvp41yIQrooNH8

from selenium import webdriver
import sys
import spotipy
import spotipy.util as util
import pprint
import requests
import json
import time
import datetime

previoussong = ""

# open log file
f = open("log.txt", "a")

while (True):

	# gets the song name
	driver = webdriver.PhantomJS()
	driver.set_window_size(1120, 550)
	driver.get("http://www.siriusxm.com/siriusxmu")
	artist = driver.find_element_by_class_name("onair-pdt-artist").text
	song = driver.find_element_by_class_name("onair-pdt-song").text
	driver.quit()

	# set up timestamp
	st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S ')

	# check to see if it is the same song
	if previoussong == song:
		time.sleep(120)
		continue

	# check to see if we got the blank/nonsongs
	if (song == "") or (artist ==  "") or (artist == "fb.com/siriusxmu") or (song == "Carles.Buzz") or (artist == "Blog Radio") or (song == "fb.com/siriusxmu") or (song == "@jennylsq") or (artist == "@HowardStern") or (artist == "#xmuoldschool") or (song == "SiriusXM U Sessions"):
		time.sleep(120)
		continue

	# check to see if song is already in log
	searchstr = song + " - " + artist
	if searchstr in open("log.txt").read():
		print st + song + " - " + artist + " already in playlist"
		previoussong = song
		time.sleep(120)
		continue
	# try the whole spotify thing

	previoussong = song

	username = "spotyams"
	playlist = "spotify:user:spotyams:playlist:6HxlZvtJfvp41yIQrooNH8"
	scope = "playlist-modify-public"

	# need to get uri of track here

	searchstring = artist + "%20" + song
	searchstring.replace(" ", "%20")
	r = requests.get('https://api.spotify.com/v1/search?q=' + searchstring  +'&type=track&limit=1&market=US')
	results = r.text
	parsedresults = json.loads(results)


	try:
		tracks = parsedresults["tracks"]
		items = tracks["items"]
		items = items[0]
		uri = items["uri"]
	except Exception, e:
		print st + song + " - " + artist + " not available on spotify"
		f.write(st + song + " - " + artist + " [NA]\n")
		time.sleep(120)
		continue
	uri.encode('ascii')

	tracks = [x.encode('UTF8') for x in uri]
	fixeduri = ''
	for x in tracks:
		fixeduri = fixeduri + x
	tracks = [fixeduri]

	token = spotipy.util.prompt_for_user_token(username, scope)

	if token:
	    sp = spotipy.Spotify(auth=token)
	    sp.trace = False
	    results = sp.user_playlist_add_tracks(username, playlist, tracks)
	    print st + song + " - " + artist + " added to playlist."
	    f.write(st + song + " - " + artist + "\n")
	else:
	    print "Can't get token for", username
	time.sleep(120)


