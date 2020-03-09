import pandas as pd
import sys
import os
import lib.etl.dfHelper as dfHelper
import lib.utils.videoHelper as videoHelper
from lib.etl.sqlConnection import sqlConnectionSetup, urlExists, columnForURLFilled, getEngine

# Run unit tests first
os.system('python test.py -v')

# Pass `python main.py log` as optional arg to see print statements
TESTING = False
if len(sys.argv) == 3:
    if sys.argv[2] == 'log':
        TESTING = True

print("IS TEST:", TESTING)
engine = getEngine(TESTING)

url = sys.argv[1]
print("Link: ", url)
window_size = 4
overlap = 2
column_name = 'pitch'
video = videoHelper.videoObject(url, window_size, overlap, TESTING)

#Check if video already exists
url_exists = urlExists(url, engine)
if url_exists == False: 
    print("This url is not in `labelled` yet:", url)
    print("Do cd 'import-clips' and run 'npm start", url ,"'")
    exit()
#Check if column already filled
column_filled = columnForURLFilled(url, engine, column_name)
if column_filled == True: print("This column has already been filled for specific URL. Will overwrite ", column_name, " data.")
video.getAudio()
print('Getting Pitch...')
video.getPitchAnalysis(dfHelper.getStartEndTimes(url, engine))
print('Got Pitch\n')
print('Updating DB for Pitch...\n')
dfHelper.updateDBWithDataFromDF(video.pitch_list, engine, column_name)
print('Done Updating')
    

