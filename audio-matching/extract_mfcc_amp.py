import utils.dbHelper as dbHelper
from moviepy.editor import *
from pytube import YouTube
from numpy import save
import sys
import librosa
import numpy as np
import os.path
import utils.librosaHelper as libHelper
import time
from sklearn import preprocessing

# USAGE python extract_mffc_amp.py [insert youtube url]
fullVidUrl = sys.argv[1]

# begin timer
exec_start = time.time()

# get youtube ids
fullId = fullVidUrl.replace('https://www.youtube.com/watch?v=', '')

# Download both videos
print("Downloading videos")
YouTube(fullVidUrl).streams[0].download("videos/", fullId)

# Extract audio
fullVideoPath = "videos/{:}.mp4".format(fullId)

fullVideo = VideoFileClip(fullVideoPath)
fullVideoAudio = fullVideo.audio

# write audio to file if audio doesn't already exist
fullAudioPath = "audio/{:}.mp3".format(fullId)

if not os.path.isfile(fullAudioPath):
  print("saving: ", fullAudioPath)
  fullVideoAudio.write_audiofile(fullAudioPath)

# convert audio to librosa and save
print("converting audio to librosa")
fullLibPath = "librosas/{:}.npy".format(fullId)

fullAudioLib, sampleRate = libHelper.extractLibrosa(fullAudioPath, fullLibPath)

# normalize
fullAudioLib = preprocessing.scale(fullAudioLib)

# Get full video intervals from db
print('Getting intervals')
intervals = dbHelper.getIntervals(fullVidUrl)

# Get mfcc and amp
print('Processing MFCC and Amplitude')
ampsAndMfccs = np.array([])
for (start, end) in intervals:
  clip = fullAudioLib[start*sampleRate : end*sampleRate]
  mfccProcessed, amplitude = libHelper.getAmpMfcc(clip, sampleRate)
  payload = [start, end, amplitude, np.array_str(mfccProcessed)]
  ampsAndMfccs = np.append(ampsAndMfccs, payload)

save("mfccs-amp-intervals/{:}.npy".format(fullId), ampsAndMfccs)
print(ampsAndMfccs)

print("COMPLETE --- %s seconds ---" % (time.time() - exec_start))
