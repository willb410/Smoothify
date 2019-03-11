import numpy as np
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy import types
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from connections import password

def playlist_model(playlist_features, track):
    #add column to label playlist tracks as true
    #import feature data from csv
    #add test track
    #normalize
    #seperate test track
    #run split training and test data
    #run the model
