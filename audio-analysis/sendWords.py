import pandas as pd
import sys
import os
import validators
import lib.etl.dfHelper as dfHelper
import lib.utils.videoHelper as videoHelper
from lib.etl.sqlConnection import sqlConnectionSetup, urlExists, columnForURLFilled, getEngine

# Run unit tests first
os.system('python test.py -v')
trump_video = "https://www.youtube.com/watch?v=JZRXESV3R74"

# Pass `python main.py log` as optional arg to see print statements
# Example input: $ python sendWords.py "https://www.youtube.com/watch?v=hC5nKPHAojw" log
TESTING = False
url = sys.argv[1]
if len(sys.argv) == 3:
    if sys.argv[2] == 'log':
        TESTING = True
    if validators.url(sys.argv[1]):
        url = sys.argv[1]
if len(sys.argv) == 2:
    url = trump_video
    if validators.url(sys.argv[1]):
        url = sys.argv[1]
    if sys.argv[1] == 'log':
        TESTING = True


print("IS TEST:", TESTING)
engine = getEngine(TESTING)

print("Link: ", url)
window_size = 4
overlap = 2
column_name = 'word'
video = videoHelper.videoObject(url, window_size, overlap, TESTING)

#Check if video already exists
url_exists = columnForURLFilled(url, engine, column_name)
if url_exists == True:
    print("This video is already in the database. Will overwrite ", column_name, " data.")
video.getAudio()
print('Getting text analysis...')
video.getTextAnalysis()
print('Got text analysis\n')
print('Updating DB for text analysis...\n')
text_columns = ['word', 'subjectivity', 'polarity']
for column in text_columns:
    dfHelper.updateDBWithDataFromDF(video.word_list, engine, column)
print('Done Updating')