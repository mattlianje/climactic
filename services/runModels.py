import numpy as np
import pandas as pd
import pickle

def getRandomForestPredictions(X):
  model_datastore = 'datastore/models/highlight-models/'
  rf_model = pickle.load(open(model_datastore + 'rf_100t.sav', 'rb')) # Get model from file
  output = rf_model.predict(X)
  
  return np.array(output)

def getNeuralNetworkPredictions(X):
  model_datastore = 'datastore/models/highlight-models/'
  nn_model = pickle.load(open(model_datastore + 'nn_2layers_0.5.sav', 'rb')) # Get model from file
  output = nn_model.predict_classes(X)
  
  return np.array(output)
