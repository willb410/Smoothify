import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from connections import password, client_id, client_secret
#from flask import Flask, jsonify,render_template
import json

def pull(id):
    features = {}
    client_credentials_manager = SpotifyClientCredentials(
        client_id='7b0e5ed233304809ae9933fd28fb4ee8', 
        client_secret='4eed3ec87a9d495abb015fce79cf5314')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    #spotify = spotipy.Spotify()    
    results = sp.audio_features(id)
    #print(results)
    for i in results:
        features = {
            "id": i['id'],
            "duration_ms": i['duration_ms'],
            "key": i['key'],
            "mode": i['mode'],
            "time_signature": i['time_signature'],
            "acousticness": i['acousticness'],
            "danceability": i['danceability'],
            "energy": i['energy'],
            "instrumentalness": i['instrumentalness'],
            "liveness": i['liveness'],
            "loudness": i['loudness'],
            "speechiness": i['speechiness'],
            "valence": i['valence'],
            "tempo": i['tempo']
        }
    return features

test = '06AKEBrKUckW0KREUWRnvT'
pull(test)