import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import sys
sys.path
sys.path.append('../')
from connections import password, client_id, client_secret
from song_features import feature_pull_df

def playlist_track_features(playlist, display_name):
    # Client credentials
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, 
        client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Search for the specified playlist by name
    p_list = sp.search(q = playlist, type = 'playlist')
    
    # Iterate through each search result to find ids playlist matching display name 
    for i in range(0, len(p_list['playlists']['items'])):
        # Choose playlist based on match of display name
        if p_list['playlists']['items'][i]['owner']['display_name'] == display_name:
            playlist_id =  p_list['playlists']['items'][0]['id']
            user_id = p_list['playlists']['items'][0]['owner']['id']
    # print(f" playlist_id: {playlist_id} | user_id: {user_id}")

    # Return playlist tracks with user and playlist id
    playlist_tracks = sp.user_playlist_tracks(user = user_id, playlist_id = playlist_id)

    # Grab ids for each track in the playlist
    playlist_track_ids = []
    for i in range(0, len(playlist_tracks['items'])):
        playlist_track_ids.append(playlist_tracks['items'][i]['track']['id'])

    # Return feature data as a Pandas DataFrame formatted for model processing
    df = feature_pull_df(playlist_track_ids)

    return df

# df = playlist_track_features('Everything Good', 'Inger Laisy Niemi')
# print(df)