'''this is just a blank app that does nothing, just to test the flask template'''

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, jsonify, render_template, request, redirect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from connections import password, client_id, client_secret
import numpy as np
import pymysql
pymysql.install_as_MySQLdb()
import requests
import pandas as pd
import sys
import song_id_search
import song_features
sys.path.append("static/js")
sys.path.append("static/css")
sys.path.append("static/Images")

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
    features = song_features.pull(song_id)
    return render_template("index.html", features=features)

#  Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
