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
from song_features import feature_pull_df
from Run_Model import run_model
from connections import password, client_id, client_secret


# Load Model
top_model = load_model("Feature_Model_Trained.h5")

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
    songs = {}
    if request.method == "POST":
        song = request.form["song"]
    songs = song_id_search.identify(song)
    return render_template("index.html", songs=songs)

@app.route("/<song_id>")
def get_features(song_id):
    features = feature_pull_df(song_id)
    return render_template("index.html", features=features)

@app.route("/feature_test")
def feat():
    # Run model
    prediction = run_model('5J5PXmMdQ2nh1lZOal8KmK', model = top_model)
    print(f" THIS IS THE PREDICTION: {prediction}")
    return jsonify(prediction)

#  Define main behavior
if __name__ == "__main__":
    app.run(debug = False, threaded = False)
''' debug and threaded set to False to properly run model'''