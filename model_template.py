import numpy as np
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy import types
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from connections import password

import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Establish SQL connection
connection_string = (f"root:{password}@localhost/spot_db")
engine = create_engine(f"mysql://{connection_string}")# , pool_recycle=3600, pool_pre_ping=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
_features = Base.classes.features
_top = Base.classes.top_200_daily
# Create connection object
session = Session(engine)

features = pd.read_sql(session.query(_features).statement, session.bind)
top = pd.read_sql(session.query(_top).statement, session.bind)

features['label'] = features.ID.isin(top.ID)
X = features.drop(['label', 'index', 'ID'], axis = 1)
y = features['label']


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from keras.utils import to_categorical
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


from keras.models import Sequential
from keras.layers import Dense
def base_model(X_train_scaled = X_train_scaled, y_train_categorical = y_train_categorical, units_1 = 50, units_2 = 30):
    # Create model and add layers
    model = Sequential()
    model.add(Dense(units=units_1, activation='relu', input_dim=13))
    model.add(Dense(units=units_2, activation='relu'))
    # model.add(Dense(units=10, activation='relu'))
    model.add(Dense(units=2, activation='softmax'))
    # Compile and fit the model
    model.compile(optimizer = 'adam',
                loss = 'categorical_crossentropy',
                metrics = ['accuracy'])
    model.fit(X_train_scaled, 
            y_train_categorical,
            epochs = 10,
            shuffle = True,
            verbose = 2)

    return model

model_1 = base_model()
model_2 = base_model(units_1=10, units_2=5)
model_3 = base_model(units_1=100, units_2=70)
model_4 = base_model(units_1=40, units_2=12)
model_5 = base_model(units_1=62, units_2=34)
model_6 = base_model(units_1=85, units_2=38)
model_7 = base_model(units_1=75, units_2=30)
model_8 = base_model(units_1=7, units_2=3)
model_9 = base_model(units_1=20, units_2=18)
model_10 = base_model(units_1=200, units_2=150)
models = [model_1, model_2, model_3,model_4, model_5, model_6, model_7, model_8,model_9, model_10]

def model_evaluation(model):
    model_loss, model_accuracy = model.evaluate(
        X_test_scaled, y_test_categorical, verbose=2)
    print(f"Normal Neural Network - Loss: {model_loss}, Accuracy: {model_accuracy}")

def predictions(model, X_test_scaled = X_test_scaled, y_test = y_test):
    encoded_predictions = model.predict_classes(X_test_scaled[400:410])
    prediction_labels = label_encoder.inverse_transform(encoded_predictions)
    print(f"Predicted classes: {prediction_labels}")
    print(f"Actual Labels:     {list(y_test[400:410])}")


for model in models:
    model_evaluation(model)

# for model in models:
#     predictions(model)