from numpy import save
from sklearn import preprocessing
import services.videoDownloader as videoDownloader
import services.mfccExtractor as mfccExtractor
import helpers.librosaHelper as librosaHelper
import helpers.dbHelper as dbHelper
import os.path
import time
import numpy as np
import sys

# USAGE test.py [youtube url to full video] [youtuble url to highlight video]
fullVidUrl = sys.argv[1]
highlightUrl = sys.argv[2]

# get youtube ids
fullId = fullVidUrl.replace('https://www.youtube.com/watch?v=', '')
highlightId = highlightUrl.replace('https://www.youtube.com/watch?v=', '')

# Check db to see if url exists
if not dbHelper.urlExists(fullVidUrl):
  print('youtube url does not exist')
  exit()

# preprocess to get librosa of full video
fullVideoPath = videoDownloader.getVideoPath(fullId)
fullAudioPath = videoDownloader.getAudioPath(fullId)
fullLibPath = librosaHelper.getLibrosaPath(fullId)

# if librosa already exists dont download video
if os.path.isfile(fullLibPath):
  fullAudioLib, sampleRate = librosaHelper.loadLibrosa(fullLibPath)

else:
  # download video
  videoDownloader.downloadVid(fullVidUrl, fullId)

  # write audio
  videoDownloader.writeAudio(fullId)

  # get and write librosa
  fullAudioLib, sampleRate = librosaHelper.createLibrosa(fullAudioPath)
  librosaHelper.saveLibrosa(fullAudioLib, sampleRate, fullLibPath)


# preprocess to get librosa of highlight video
highlightVideoPath = videoDownloader.getVideoPath(highlightId)
highlightAudioPath = videoDownloader.getAudioPath(highlightId)
highlightLibPath = librosaHelper.getLibrosaPath(highlightId)

# if librosa already exists dont download video
if os.path.isfile(highlightLibPath):
  highlightAudioLib, sampleRate = librosaHelper.loadLibrosa(highlightLibPath)

else:
  # download video
  videoDownloader.downloadVid(highlightUrl, highlightId)

  # write audio
  videoDownloader.writeAudio(highlightId)

  # get and write librosa
  highlightAudioLib, sampleRate = librosaHelper.createLibrosa(highlightAudioPath)
  librosaHelper.saveLibrosa(highlightAudioLib, sampleRate, highlightLibPath)


# normalize both libs
fullAudioLib = preprocessing.scale(fullAudioLib)
highlightAudioLib = preprocessing.scale(highlightAudioLib)

# Get full video intervals from db
print('Getting intervals')
intervals = dbHelper.getIntervals(fullVidUrl)

print('Starting matching:')
exec_start = time.time()
labelledClips = np.array([])
start_idx = 0
labelledClipsFilePath = "datastore/labelled-clips/{:}.npy".format(fullId)

# loop through intervals and check if clip exists in highlight video
for (start, end) in intervals:
  clip = fullAudioLib[start*sampleRate : end*sampleRate]
  hasMatch, idx = librosaHelper.clipExistsInFull(clip, highlightAudioLib[start_idx:])

  # add labelled clip to array and save occasionally
  labelledClips = np.append(labelledClips, [start, end, hasMatch])
  if len(labelledClips) % 20 == 0:
    save(labelledClipsFilePath, labelledClips)

  # print start end time for visual checking
  startMinute, startSec = divmod(start, 60)
  endMinute, endSec = divmod(end, 60)
  print(hasMatch, idx, "{:}:{:} - {:}:{:}".format(startMinute, startSec, endMinute, endSec))
  if hasMatch:
    start_idx = start_idx + (len(clip)//2) - 1

save(labelledClipsFilePath, labelledClips)
print("COMPLETE --- %s seconds ---" % (time.time() - exec_start))
