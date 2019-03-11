# Set the file path to run Flask app
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
from flask import Flask, jsonify, render_template, request, redirect
import requests
import sys
sys.path.append("static/js")
sys.path.append("static/css")
sys.path.append("static/Images")
sys.path.append("static/img")
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import pymysql
pymysql.install_as_MySQLdb()
import numpy as np
import pandas as pd
from keras.models import load_model
import song_id_search
from song_features import pull, feature_pull_df
from Run_Model import run_model
from connections import password, client_id, client_secret
from Playlist_Model import playlist_model

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def apps():
    songs = {}
    return render_template("index.html", songs=songs)

@app.route("/send", methods=["GET", "POST"])
def send():
    global songs
    if request.method == "POST":
        song = request.form["song"]
        if len(song) > 0:
            songs = song_id_search.identify(song)
        else:
            songs = "err1"
            #print(songs)
            return render_template("index.html", songs=songs)
    #print(songs)
    return render_template("index.html", songs=songs)

@app.route("/<song_id>")
def get_features(song_id):
    global song_dict
    features = pull(song_id)
    for item in songs:
        if item['id'] == song_id:
            song_dict = item
            #print("features route song dictionary")
            #print(song_dict)
    # Run model
    # Load Model
    top_model = load_model("Feature_Model_Trained.h5")
    prediction = run_model(song_id, model = top_model)
    print(f" THIS IS THE PREDICTION: {prediction}")
    return render_template("index.html", features=features, prediction=prediction, song_id=song_id, song_dict=song_dict)

@app.route("/playlist", methods=["GET", "POST"])
def playlist():
    #print(song_dict)
    track = song_dict['id']
    #print("id is:")
    #print(song_dict['id'])
    if request.method == "POST":
        playlist = request.form["playlistName"]
        user = request.form["userName"]
        if (len(playlist) > 0) and (len(user) > 0):
            fit_result = playlist_model(playlist, user, track)
        else:
            fit_result = "err1"
            return render_template("index.html", fit_result=fit_result)
        #print("fit result is:")
        #print(fit_result == 0)
    return render_template("index.html", fit_result=fit_result, song_dict=song_dict)

#  Define main behavior
if __name__ == "__main__":
    app.run(debug = False, threaded = False)  
''' debug and threaded set to False to properly run model'''