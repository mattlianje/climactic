import utils.dbHelper as dbHelper
from moviepy.editor import *
from pytube import YouTube
from numpy import save
import sys
import librosa
import soundfile as sf
import numpy as np
import os.path
import utils.librosaHelper as libHelper
import time
from sklearn import preprocessing

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

def downloadVid(vidUrl, vidId):
  videoPath = "videos/{:}.mp4".format(vidId)
  if not os.path.isfile(videoPath):
    print("Downloading ", vidUrl)
    YouTube(vidUrl).streams[0].download("videos/", vidId)
  else:
    print(vidUrl, " already downloaded")

def writeAudio(videoPath, audioPath):
  if not os.path.isfile(audioPath):
    video = VideoFileClip(videoPath)
    audio = video.audio
    print("saving: ", audioPath)
    audio.write_audiofile(audioPath)

# preprocess to get librosa of full video
fullVideoPath = "videos/{:}.mp4".format(fullId)
fullAudioPath = "audio/{:}.mp3".format(fullId)
fullLibPath = "librosas/{:}.npy".format(fullId)

# if librosa already exists dont download video
if os.path.isfile(fullLibPath):
  fullAudioLib, sampleRate = libHelper.retrieveLibrosa(fullLibPath)

else:
  # download video
  downloadVid(fullVidUrl, fullId)

  # write audio
  writeAudio(fullVideoPath, fullAudioPath)

  # get librosa
  fullAudioLib, sampleRate = libHelper.extractLibrosa(fullAudioPath, fullLibPath)


# preprocess to get librosa of highlight video
highlightVideoPath = "videos/{:}.mp4".format(highlightId)
highlightAudioPath = "audio/{:}.mp3".format(highlightId)
highlightLibPath = "librosas/{:}.npy".format(highlightId)

# if librosa already exists dont download video
if os.path.isfile(highlightLibPath):
  highlightAudioLib, sampleRate = libHelper.retrieveLibrosa(highlightLibPath)

else:
  # download video
  downloadVid(highlightUrl, highlightId)

  # write audio
  writeAudio(highlightVideoPath, highlightAudioPath)

  # get librosa
  highlightAudioLib, sampleRate = libHelper.extractLibrosa(highlightAudioPath, highlightLibPath)

# normalize both libs
fullAudioLib = preprocessing.scale(fullAudioLib)
highlightAudioLib = preprocessing.scale(highlightAudioLib)

# Get full video intervals from db
print('Getting intervals')
intervals = dbHelper.getIntervals(fullVidUrl)

print('Starting matching:')
# dice up the full audio into 4 second intervals
exec_start = time.time()
labelledClips = np.array([])
start_idx = 0

# loop through intervals and check if clip exists in highlight video
for (start, end) in intervals:
  clip = fullAudioLib[start*sampleRate : end*sampleRate]
  hasMatch, idx = libHelper.clipExistsInFull(clip, highlightAudioLib[start_idx:])

  # add labelled clip to array and save occasionally
  labelledClips = np.append(labelledClips, [start, end, hasMatch])
  if len(labelledClips) % 20 == 0:
    save("labelled-time-intervals/{:}.npy".format(fullId), labelledClips)

  # print start end time for visual checking
  startMinute, startSec = divmod(start, 60)
  endMinute, endSec = divmod(end, 60)
  print(hasMatch, idx, "{:}:{:} - {:}:{:}".format(startMinute, startSec, endMinute, endSec))
  if hasMatch:
    start_idx = start_idx + (len(clip)//2) - 1

save("labelled-time-intervals/{:}.npy".format(fullId), labelledClips)
print("COMPLETE --- %s seconds ---" % (time.time() - exec_start))
