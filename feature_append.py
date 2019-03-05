import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from connections import client_id, client_secret

import pandas as pd
import numpy as np

import os


def feature_append(existing_ids, new_ids, db_conn):
    '''
    existing_ids: ids already in the database
    mew_ids: ids you are adding to the database
    db_conn: connection to database
    '''
    
    
    # Spotify client credentials
    client_credentials_manager = SpotifyClientCredentials(
        client_id = client_id, 
        client_secret = client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Filter out songs for which there is already feature data
    id_list = []
    for id in new_ids:
        if id not in existing_ids:
            id_list.append(id)
    


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
    unrel_keys = ['type', 'uri', 'analysis_url', 'track_href']
    for dict in audio_features:
        for key in unrel_keys:
            if key in dict:
                del dict[key]


    features_df = pd.DataFrame(audio_features)
    features_df.head()


    features_df.rename(columns = {'acousticness':'Acousticness', 'danceability':'Danceability', 
                                'duration_ms':'Duration_ms', 'energy':'Energy', 
                                'id':'ID', 'instrumentalness':'Instrumentalness', 
                                'key':'Key', 'liveness':'Liveness', 
                                'loudness':'Loudness', 'mode':'Mode', 
                                'speechiness':'Speechiness', 'tempo':'Tempo', 
                                'time_signature':'Time_Signature', 'valence':'Valence'}, inplace = True)
    
    # Export to SQL
    db_conn.execute("USE spot_db")
    features_df.to_sql(
        name = 'features', con = engine,
        if_exists = 'append', 
        dtype={'ID': types.VARCHAR(255)})


