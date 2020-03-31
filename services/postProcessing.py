# Dependencies
import numpy as np
import pandas as pd
import os

from helpers import secrets
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def getHighlightTimestamps(df, vidId):
  # Loop through DFs and send highlight timestamps to arrays
  rf_timestamps, nn_timestamps = [], []
  highlight_detected_rf, highlight_detected_nn = False, False

  for i, (index, row) in enumerate(df.iterrows()): # Here i is rowcount, we use it to know when we're on the last row
      # Get Highlights from RF predictions
      if row['pred_highlight_rf'] == 1:
          if highlight_detected_rf == False: 
              highlight_detected_rf = True
              highlight_start_rf = row['start']
              highlight_end_rf = row['end']
          else:
              highlight_end_rf = row['end']

      if row['pred_highlight_rf'] == 0 or i >= len(df) - 1:
          if highlight_detected_rf == True: 
              highlight_detected_rf = False
              rf_timestamps.append([highlight_start_rf, highlight_end_rf])

      # Get Highlights from NN predictions
      if row['pred_highlight_nn'] == 1:
          if highlight_detected_nn == False: 
              highlight_detected_nn = True
              highlight_start_nn = row['start']
              highlight_end_nn = row['end']
          else:
              highlight_end_nn = row['end']
      if row['pred_highlight_nn'] == 0 or i >= len(df) - 1:
          if highlight_detected_nn == True: 
              highlight_detected_nn = False
              nn_timestamps.append([highlight_start_nn, highlight_end_nn])

  # Save the resulting Numpy Arrays to a .npz file
  os.chdir("..")
  npzfilename = 'datastore/highlights-timestamps/' + vidId + '.npz'
  np.savez(npzfilename, rf_timestamps=rf_timestamps, nn_timestamps=nn_timestamps)

# To access the arrays:
# npzfile = np.load('highlights-arrays.npz')
# npzfile['rf_timestamps']
