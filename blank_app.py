'''this is just a blank app that does nothing, just to test the flask template'''

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, jsonify,render_template
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from connections import password
import numpy as np
import pymysql
pymysql.install_as_MySQLdb()
import requests
import pandas as pd
import sys
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
    
    return render_template("index.html")

#  Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
