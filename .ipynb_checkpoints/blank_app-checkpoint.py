'''this is just a blank app that does nothing, just to test the flask template'''

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, jsonify,render_template
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from connections import password, client_id, client_secret
import numpy as np
import pymysql
pymysql.install_as_MySQLdb()
import requests
import pandas as pd
from keras.models import load_model
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
sys.path.append("static/js")
sys.path.append("static/css")
sys.path.append("static/Images")


# Client credentials
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, 
    client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def apps():
    
    return render_template("index.html")

@app.route("/model")
def model():
    top_model = load_model("Feature_Model_Trained.h5")

    sp.audio_features('06AKEBrKUckW0KREUWRnvT')



#  Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
