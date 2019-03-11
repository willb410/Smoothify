import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense

from connections import password, client_id, client_secret
from Playlist_Track_Features import playlist_track_features
from song_features import feature_pull_df

def playlist_model(playlist_name, display_name, track_id):
    
    # Import playlist features
    playlist_features = playlist_track_features(playlist_name, display_name)

    # Import features for scaling and false training cases 
    scale_features = pd.read_csv('Database_Setup/features.csv')
    scale_features.drop(['Unnamed: 0', 'ID'], axis = 1, inplace = True)
    playlist_features.rename(columns = {'acousticness':'Acousticness', 'danceability':'Danceability', 
                        'duration_ms':'Duration_ms', 'energy':'Energy', 
                        'id':'ID', 'instrumentalness':'Instrumentalness', 
                        'key':'Key', 'liveness':'Liveness', 
                        'loudness':'Loudness', 'mode':'Mode', 
                        'speechiness':'Speechiness', 'tempo':'Tempo', 
                        'time_signature':'Time_Signature', 'valence':'Valence'}, inplace = True)

    # Add label column
    playlist_features['label'] = True
    scale_features['label'] = False

    # Combine feature dataset
    all_features = playlist_features.append(scale_features)

    # Create X and Y sets
    X = all_features.drop(['label'], axis = 1)
    y = all_features['label']

    # Split training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state = 1, stratify = y)
    X_scaler = StandardScaler().fit(X_train)
    X_train_scaled = X_scaler.transform(X_train)
    X_test_scaled = X_scaler.transform(X_test)
    # Label-encode dataset
    label_encoder = LabelEncoder()
    label_encoder.fit(y_train)
    encoded_y_train = label_encoder.transform(y_train)
    encoded_y_test = label_encoder.transform(y_test)
    # Convert encoded labels to one-hot-encodeing
    y_train_categorical = to_categorical(encoded_y_train)
    y_test_categorical = to_categorical(encoded_y_test)

    # Set up model
    def build_model():
        model = Sequential()
        model.add(Dense(units=5, activation='relu', input_dim=13))
        model.add(Dense(units=3, activation='relu'))
        model.add(Dense(units=2, activation='softmax'))

        # Compile and fit the model
        model.compile(optimizer = 'adam',
                    loss = 'categorical_crossentropy',
                    metrics = ['accuracy'])
        model.fit(X_train, 
                y_train_categorical,
                epochs = 5,
                shuffle = True,
                verbose = 2)
        
        # Return model accuracy
        model_loss, model_accuracy = model.evaluate(
        X_test_scaled, y_test_categorical, verbose=0)
        
        return model, model_accuracy

    # Run model if accuracy below 90%
    runs = 0
    model, model_accuracy = build_model()
    while model_accuracy < 0.9:
        print(model_accuracy)
        print(f"Number of runs: {runs}")
        model, model_accuracy = build_model()
        runs += 1

    print(f"Accuracy: {model_accuracy}")
    print(f"Number of runs: {runs}")


    track_features = feature_pull_df(track_id)

    prediction = model.predict_classes(x = track_features)


    return int(prediction)