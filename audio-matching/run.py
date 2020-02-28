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

# Download both videos
print("Downloading videos")
YouTube(fullVidUrl).streams[0].download("videos/", "full_video")
YouTube(highlightUrl).streams[0].download("videos/", "highlight_video")

# Extract audio
fullVideoPath = "videos/full_video.mp4"
highlightVideoPath = "videos/highlight_video.mp4"

fullVideo = VideoFileClip(fullVideoPath)
fullVideoAudio = fullVideo.audio
fullDuration = fullVideo.duration

highlightVideo = VideoFileClip(highlightVideoPath)
highlightVideoAudio = highlightVideo.audio
highlightDuration = highlightVideoAudio.duration

# write audio to file if audio doesn't already exist
fullAudioPath = "audio/{:}_full_audio.mp3".format(fullId)
highlightAudioPath = "audio/{:}_highlight_audio.mp3".format(highlightId)

if not os.path.isfile(fullAudioPath):
  print("saving: ", fullAudioPath)
  fullVideoAudio.write_audiofile(fullAudioPath)

if not os.path.isfile(highlightAudioPath):
  print("saving: ", highlightAudioPath)
  highlightVideoAudio.write_audiofile(highlightAudioPath)

# convert audio to librosa and save
print("converting audio to librosa")
fullLibPath = "librosas/{:}_full.npy".format(fullId)
highlightLibPath = "librosas/{:}_highlight.npy".format(highlightId)

fullAudioLib, sampleRate = libHelper.extractLibrosa(fullAudioPath, fullLibPath)
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

# loop through intervals and check if clip exists in highlight video
for (start, end) in intervals:
  clip = fullAudioLib[start*sampleRate : end*sampleRate]
  hasMatch, idx = libHelper.clipExistsInFull(clip, highlightAudioLib)

  # add labelled clip to array and save occasionally
  labelledClips = np.append(labelledClips, [start, end, hasMatch])
  if len(labelledClips) % 20 == 0:
    save("labelled-time-intervals/{:}.npy".format(fullId), labelledClips)

  # print start end time for visual checking
  startMinute, startSec = divmod(start, 60)
  endMinute, endSec = divmod(end, 60)
  print(hasMatch, idx, "{:}:{:} - {:}:{:}".format(startMinute, startSec, endMinute, endSec))

save("labelled-time-intervals/{:}.npy".format(fullId), labelledClips)
print("COMPLETE --- %s seconds ---" % (time.time() - exec_start))
