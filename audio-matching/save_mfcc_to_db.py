import utils.dbHelper as dbHelper
import sys
import os.path
from numpy import load
import numpy as np

# USAGE python save_to_db.py [youtube url]
vidUrl = sys.argv[1]

# get youtube id
vidId = vidUrl.replace('https://www.youtube.com/watch?v=', '')

# Check if mfcc data for the video is saved locally
mfccPath = "mfccs-amp-intervals/{:}.npy".format(vidId)

if not os.path.isfile(mfccPath):
  print('Mfcc data not found, make sure url is right and file exists')
  exit()

# load data

# mfcc and amp data format: [start, end, amplitude, mfcc as string]
print('loading mfcc, amp data')
mfccData = load(mfccPath)

rows = len(mfccData) // 4
mfccData = mfccData.reshape(rows, 4)

# iterate through mfcc amp data and generate query

# convert mfccData to query syntax in the for of (url, start, mfcc, amp)
def formatUpdatedValues(url, start, end, mfcc, amplitude):
  return "('{:}', {:}, {:}, '{:}', {:})".format(url, start, end, mfcc, amplitude)

# loop through mfccData, build array of update string
updatedValues = []
for (start, end, amplitude, mfcc_string) in mfccData:
  valuesString = formatUpdatedValues(vidUrl, start, end, mfcc_string, amplitude)
  updatedValues.append(valuesString)

# build query sytax
querySyntax = """ INSERT INTO labelled (url, start, end, mfcc, amplitude)
                  VALUES
                    {:}
                  ON DUPLICATE KEY UPDATE
                    mfcc = VALUES(mfcc),
                    amplitude = VALUES(amplitude);""".format(",".join(updatedValues))

# update rows in db
print('updating rows')
dbHelper.batchUpdate(querySyntax)
print('FINISHED')
