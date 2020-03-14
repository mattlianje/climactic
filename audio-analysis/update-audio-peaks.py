import pandas as pd
import sys
import os
import validators
from tqdm import tqdm
import lib.etl.dfHelper as dfHelper
import lib.utils.videoHelper as videoHelper
from lib.etl.sqlConnection import sqlConnectionSetup, urlExists, columnForURLFilled, getEngine, getTableAsDf
from scipy.signal import find_peaks
import plotly.graph_objects as go
from scipy.signal import argrelextrema
import numpy as np

# Run unit tests first
os.system('python test.py -v')

IS_TEST = False
if len(sys.argv) == 2:
    if sys.argv[1] == 'log':
        IS_TEST = True

print("IS TEST:", IS_TEST)
engine = getEngine(IS_TEST)

print('Getting labelled DF ...')
# Getting the labelled table as pandas df.
labelled_df = getTableAsDf("labelled", engine)
# Hackedy hack ...
clean_labelled_df = labelled_df.rename(columns={'start': 'start_time_s'})
# Get the list of urls for which amplitude is NOT NULL and is_amplitude_peak is NULL.
filtered_labelledDF = labelled_df[(labelled_df['amplitude'].notnull()) & (labelled_df['is_amplitude_peak'].isnull())]
url_list = filtered_labelledDF.url.unique()
if len(url_list) == 0:
    print('All videos already have amplitude peak tags!')
else:
    print('Going through videos with is_amplitude_peak tag ...')
    column_name = 'is_amplitude_peak'
    for url in tqdm(url_list):
        temp_df = clean_labelled_df[clean_labelled_df['url'] == url].sort_values(by='start_time_s', ascending=True)
        # indices <- list of time stamps of amplitude peaks
        time_series = temp_df['amplitude']
        indices = find_peaks(time_series, distance=30, )[0]
        for index, row in temp_df.iterrows():
            if row['start_time_s'] not in indices:
                temp_df.at[index, 'is_amplitude_peak'] = False
            else:
                temp_df.at[index, 'is_amplitude_peak'] = True
        dfHelper.updateDBWithDataFromDF(temp_df, engine, column_name)
    print('Done!')

fig = go.Figure()
fig.add_trace(go.Scatter(
    y=time_series,
    mode='lines+markers',
    name='Original Plot'
))

fig.add_trace(go.Scatter(
    x=indices,
    y=[time_series[j] for j in indices],
    mode='markers',
    marker=dict(
        size=8,
        color='red',
        symbol='cross'
    ),
    name='Detected Peaks'
))

fig.show()
