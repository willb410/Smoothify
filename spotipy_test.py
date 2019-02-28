import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from flask import Flask, jsonify,render_template

import json

client_credentials_manager = SpotifyClientCredentials(
    client_id='7b0e5ed233304809ae9933fd28fb4ee8', 
    client_secret='4eed3ec87a9d495abb015fce79cf5314')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
spotify = spotipy.Spotify()

name = 'Vampire Weekend'
results = sp.audio_features('06AKEBrKUckW0KREUWRnvT')
# print(results)

app = Flask(__name__)

@app.route("/analysis")
def testo():
    # audio_features, audio_analysis
    
    results = sp.audio_analysis('06AKEBrKUckW0KREUWRnvT')
    
    return jsonify(results)

@app.route("/categories")
def categorical():
    # categories

    results = sp.user_playlist_tracks(user = 'spotifycharts', playlist_id = '37i9dQZEVXbKuaTI1Z1Afx', fields = 'items(track(name, id))')

    return jsonify(results)


#  Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
