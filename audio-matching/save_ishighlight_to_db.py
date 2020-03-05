import utils.dbHelper as dbHelper
import sys
import os.path
from numpy import load
import numpy as np

# USAGE python save_to_db.py [youtube url]
vidUrl = sys.argv[1]

# get youtube id
vidId = vidUrl.replace('https://www.youtube.com/watch?v=', '')

# Check if labelled data for the video is saved locally
labelledPath = "labelled-time-intervals/{:}.npy".format(vidId)

if not os.path.isfile(labelledPath):
  print('isHighlight data not found, make sure url is right and file exists')
  exit()

# load data
# labelled data format: [start, end, isHighlight]
print('loading data')
isHighlightData = load(labelledPath)

rows = len(isHighlightData) // 3
isHighlightData = isHighlightData.reshape(rows, 3)

# convert mfccData to query syntax in the for of (url, start, isHighlight)
def formatUpdatedValues(url, start, end, isHighlight):
  return "('{:}', {:}, {:}, {:})".format(url, start, end, isHighlight)

# loop through mfccData, build array of update string
updatedValues = []
for (start, end, isHighlight) in isHighlightData:
  valuesString = formatUpdatedValues(vidUrl, int(start), int(end), int(isHighlight))
  updatedValues.append(valuesString)

# build query sytax
querySyntax = """ INSERT INTO labelled (url, start, end, isHighlight)
                  VALUES
                    {:}
                  ON DUPLICATE KEY UPDATE
                    isHighlight = VALUES(isHighlight);""".format(",".join(updatedValues))

# update rows in db
print('updating rows')
dbHelper.batchUpdate(querySyntax)
print('FINISHED')
