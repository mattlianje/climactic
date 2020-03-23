# Dependencies
import numpy as np
import pandas as pd
import secrets

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# Get URL for which we want to do post-processing
url = 'https://www.youtube.com/watch?v=-5NzaAt_wY0' # We would get this as a variable but hard-coded for now


# Connect to DB and get appropriate information for URL
db_conn_str = "mysql+pymysql://{:}:{:}@{:}/{:}".format(secrets.user, secrets.password, secrets.host, secrets.db)
db_conn = create_engine(db_conn_str)
df = pd.read_sql('SELECT * FROM predictions_table WHERE url="'+ url +'"', con=db_conn)

# Loop through DFs and send highlight timestamps to arrays
rf_timestamps, nn_timestamps = [], []
highlight_detected_rf, highlight_detected_nn = False, False

for index, row in df.iterrows():
    # Get Highlights from RF predictions
    if row['pred_highlight_rf'] == 1:
        if highlight_detected_rf == False: 
            highlight_detected_rf = True
            highlight_start_rf = row['start']
            highlight_end_rf = row['end']
        else:
            highlight_end_rf = row['end']
    else:
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
    else:
        if highlight_detected_nn == True: 
            highlight_detected_nn = False
            nn_timestamps.append([highlight_start_nn, highlight_end_nn])


# Call the the following variables for a list of list of highlight timestamps (depending on the model)
rf_timestamps
nn_timestamps