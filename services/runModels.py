import numpy as np
import pandas as pd
import pickle

def getRandomForestPredictions(X):
  rf_model = pickle.load(open('highlight-model/rf_100t.sav', 'rb')) # Get model from file
  output = rf_model.predict(X)
  
  return np.array(output)

def getNeuralNetworkPredictions(X):
  nn_model = pickle.load(open('nn_2layers_0.5.sav', 'rb')) # Get model from file
  output = nn_model.predict_classes(X)
  
  return np.array(output)