import spotipy
from connections import password, client_id, client_secret
from spotipy.oauth2 import SpotifyClientCredentials
#from flask import Flask, jsonify,render_template
import json
client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, 
        client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def identify(track):
    songs = []
    track_info = sp.search(q=' track:' + track, type='track')
    print(track_info["tracks"]["items"][0]['id'])
    print(track_info["tracks"]["items"][0]['name'])
    print(track_info["tracks"]["items"][0]['album']['artists'][0]['name']) 
    print(track_info['tracks']['total']) 
    print("==========")
    if track_info['tracks']['total'] == 0:
        songs[track]: "No Results"
    else:
        for i in track_info["tracks"]["items"]:
            id = i["id"] 
            #print(id)
            artist = i['album']['artists'][0]['name'] 
            #print(artist)
            name = i['name'] 
            #print(name)
            #songs[id] = "test"
            songs.append({
                "id": id,
                "name": name,
                "artist": artist
            })
        #print(songs)
    return songs

""" test = "myxomatosis"
identify(test) """