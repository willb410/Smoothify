import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from connections import password, client_id, client_secret
import song_id_search
import song_features

import pandas as pd

def feature_pull_df(ids = []):
    ''' Ready to be processed for model '''
    client_credentials_manager = SpotifyClientCredentials(
    client_id = client_id, 
    client_secret = client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        
    id_list = ids
    # Divide list of Ids into chunks of 100
    def chunk_lists(list, n = 100): 
        for i in range(0, len(list), n):  
            yield list[i:i + n] 
    # Must wrap output in list()
    id_chunks = list(chunk_lists(id_list))


    audio_features = []
    for ids in id_chunks:
        audio_feature = sp.audio_features(tracks = ids)

        audio_features.append(audio_feature)

    # Remove sublists
    audio_features = [item for sublist in audio_features for item in sublist]


    # Delete irrelevant categories
    unrel_keys = ['id', 'type', 'uri', 'analysis_url', 'track_href']
    for dict in audio_features:
        for key in unrel_keys:
            if key in dict:
                del dict[key]


    features_df = pd.DataFrame(audio_features)

    return features_df

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