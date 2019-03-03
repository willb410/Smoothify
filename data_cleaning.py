import pandas as pd
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
from mysql_conn import password
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
import json
import numpy as np

# Change working directory to file location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Client credentials
client_credentials_manager = SpotifyClientCredentials(
    client_id='7b0e5ed233304809ae9933fd28fb4ee8', 
    client_secret='4eed3ec87a9d495abb015fce79cf5314')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Today
import datetime
current_date = datetime.datetime.today().strftime('%Y-%m-%d')

playlist_ids = {'United States Viral 50':'37i9dQZEVXbKuaTI1Z1Afx'} #,
                #'United States Top 50':'37i9dQZEVXbLRQDuF5jeBp'}

playlist_tracks = [current_date]

for name, id in playlist_ids.items():
    results = sp.user_playlist_tracks(user = 'spotifycharts', playlist_id = id, fields = 'items(track(name, id, artists))')
    
    tracks = []
    track_id = []
    track_name = []
    track_artist = []
    for result in results['items']:
        tracks.append([result['track']['name'], result['track']['id']])
        track_id.append(result['track']['id'])
        track_name.append(result['track']['name'])
        artist_dict = result['track']['artists'][0]
        track_artist.append(artist_dict['name'])
    playlist_tracks.append([name, tracks])

songs = pd.DataFrame(np.column_stack([track_id, track_name, track_artist]), 
                               columns=['Id', 'Track_Name', 'Artist'])
#print(songs)

# First element shows date for 0th element or changes playlist
# Third element changes song within each playlist
song_id = playlist_tracks[1][1][0][1]
song_name = playlist_tracks[1][1][0][0]

#print(f'song id: {song_id}')
#print(f'song name: {song_name}')
f_id = []
f_duration_ms = []
f_key = []
f_mode = []
f_Time_Signature = []
f_acousticness = []
f_danceablity = []
f_energy = []
f_instrumentalness = []
f_liveness = []
f_loudness = []
f_speechiness = []
f_valence = []
f_tempo = []

playlist_audio_features = []
for playlist in playlist_tracks[1:]:
    tracks = []

    # Create list of ids for each playlist with max of 50 ids
    id = []
    for i in range(0, len(playlist[1])): 
        id.append(playlist[1][i][1])
    
    # list of playlist ids
    tracks.append(id)
    audio_feature = sp.audio_features(tracks = tracks[0])
    #print(audio_feature)
    # Add audio feature for song to dictionary
    playlist_audio_features.append(audio_feature)
    print(f'length of audio_feature: {len(audio_feature)}')
    for i in range(0, len(audio_feature)): 
        feature_dict = audio_feature[i]
        f_id.append(feature_dict['id'])
        f_duration_ms.append(feature_dict['duration_ms'])
        f_key.append(feature_dict['key'])
        f_mode.append(feature_dict['mode'])
        f_Time_Signature.append(feature_dict['time_signature'])
        f_acousticness.append(feature_dict['acousticness'])
        f_danceablity.append(feature_dict['danceability'])
        f_energy.append(feature_dict['energy'])
        f_instrumentalness.append(feature_dict['instrumentalness'])
        f_liveness.append(feature_dict['liveness'])
        f_loudness.append(feature_dict['loudness'])
        f_speechiness.append(feature_dict['speechiness'])
        f_valence.append(feature_dict['valence'])
        f_tempo.append(feature_dict['tempo']) 
        


#playlist_audio_features
#print(playlist_audio_features[0])
Features = (pd.DataFrame(np.column_stack([f_id, f_duration_ms, f_key, f_mode, f_Time_Signature,
            f_acousticness, f_danceablity, f_energy, f_instrumentalness, f_liveness, f_loudness, f_speechiness, f_valence, f_tempo]), 
            columns=(['Id','Duration_ms','Key','Mode','Time_Signature','Acousticness','Danceablity','Energy','Instrumentalness','Liveness','Loudness','Speechiness','Valence','tempo'])))

#print(Features)

# # SQFT Dataset
# # MySQL Connection
# Define database within MySQL client
connection_string = (f"root:{password}@localhost")
engine = create_engine(f"mysql://{connection_string}")
engine.execute("DROP DATABASE IF EXISTS music")
engine.execute("CREATE DATABASE music")
engine.execute("USE music")

engine.execute("USE music")
(songs.to_sql(
    name = 'songs', con = engine, chunksize = 75))
    #if_exists = 'replace', chunksize = 75))
with engine.connect() as con:
    con.execute('ALTER TABLE `songs` modify Id VARCHAR(22);')
    con.execute('ALTER TABLE `songs` ADD PRIMARY KEY (`Id`);')

engine.execute("USE music")
(Features.to_sql(
    name = 'Features', con = engine)) #,
    #if_exists = 'replace'))
with engine.connect() as con:
    con.execute('ALTER TABLE `Features` modify Id VARCHAR(22);')
    con.execute('ALTER TABLE `Features` ADD PRIMARY KEY (`Id`);')