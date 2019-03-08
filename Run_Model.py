import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from connections import password, client_id, client_secret
import song_id_search
from song_features import feature_pull_df

import pandas as pd

from keras.models import load_model
from sklearn.preprocessing import LabelEncoder, StandardScaler
from keras import backend as K 


def run_model(id, model):
    
    # Import
    X = feature_pull_df(id)
    # top_model = load_model("Feature_Model_Trained.h5")
    top_model = model
    
    # Grab feature data for scaling context
    scale_features = pd.read_csv('Database_Setup/features.csv')
    scale_features.drop(['Unnamed: 0', 'ID'], axis = 1, inplace = True)
    X.rename(columns = {'acousticness':'Acousticness', 'danceability':'Danceability', 
                                    'duration_ms':'Duration_ms', 'energy':'Energy', 
                                    'id':'ID', 'instrumentalness':'Instrumentalness', 
                                    'key':'Key', 'liveness':'Liveness', 
                                    'loudness':'Loudness', 'mode':'Mode', 
                                    'speechiness':'Speechiness', 'tempo':'Tempo', 
                                    'time_signature':'Time_Signature', 'valence':'Valence'}, inplace = True)
    all_features = X.append(scale_features)
    
    # Normalize data
    X_scaler = StandardScaler().fit(all_features)
    predict = X_scaler.transform(all_features)
    normal_predict = pd.DataFrame(predict)

    # Grab the test feature
    predict_feature = normal_predict.head(1)

    # Run model
    prediction = top_model.predict_classes(x = predict_feature)
    K.clear_session()
    return int(prediction)

# Load Model
top_model = load_model("Feature_Model_Trained.h5")
# test
print(f"THIS IS THE PREDICTION: {run_model('5J5PXmMdQ2nh1lZOal8KmK', top_model)}")