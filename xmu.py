
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



xmu = False
bridge = False
outlaw = False
if len(sys.argv) < 2:
    print('usage: python xmu.py [xmu|bridge|outlaw]')
    sys.exit()
elif sys.argv[1] == "xmu":
    xmu = True
    logfile = "log.txt"
elif sys.argv[1] == "bridge":
    bridge = True
    logfile = "bridgelog.txt"
elif sys.argv[1] == "outlaw":
    outlaw = True
    logfile = "outlawlog.txt"
else:
    print('usage: python xmu.py [xmu|bridge]')
    sys.exit()

# open log file
f = open(logfile, "a")

username = "spotyams"
scope = "playlist-modify-public"
if xmu:
    playlist = "spotify:user:spotyams:playlist:6HxlZvtJfvp41yIQrooNH8"
elif bridge:
    playlist = "spotify:user:spotyams:playlist:4BP5BgV2rTN3jmRAEeqyxd"
else:
    playlist = "spotify:user:spotyams:playlist:6Z0OOKpV5APyfsycNgbDF3"

token = spotipy.util.prompt_for_user_token(username, scope)

if not token:
    print "Can't get token for", username

while (True):

    # gets the song name
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)
    if xmu:
        driver.get("http://www.siriusxm.com/siriusxmu")
    elif bridge:
        driver.get("http://www.siriusxm.com/thebridge")
    else:
        driver.get("http://www.siriusxm.com/outlawcountry")
        
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
    if xmu:
        if (song == "") or (artist ==  "") or (artist == "fb.com/siriusxmu") or (song == "Carles.Buzz") or (artist == "Blog Radio") or (song == "fb.com/siriusxmu") or (song == "@jennylsq") or (artist == "@HowardStern") or (artist == "#xmuoldschool") or (song == "SiriusXM U Sessions"):
            time.sleep(120)
            continue
    else:
        if (song == "") or (artist ==  ""):
            time.sleep(120)
            continue

    # check to see if song is already in log
    searchstr = song + " - " + artist

    if searchstr in open(logfile).read():
        print st + song + " - " + artist + " already in playlist"
        previoussong = song
        time.sleep(120)
        continue
    # try the whole spotify thing

    previoussong = song

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
        f.flush()
        time.sleep(120)
        continue
    uri.encode('ascii')

    tracks = [x.encode('UTF8') for x in uri]
    fixeduri = ''
    for x in tracks:
        fixeduri = fixeduri + x
    tracks = [fixeduri]

    token = spotipy.util.prompt_for_user_token(username, scope)

    
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.user_playlist_add_tracks(username, playlist, tracks)
    print st + song + " - " + artist + " added to playlist."
    f.write(st + song + " - " + artist + "\n")
    f.flush()
    
    time.sleep(120)


