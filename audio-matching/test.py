import sys
import librosa
import os.path
import numpy as np
from moviepy.editor import *
import matplotlib.pyplot as plt
from sklearn import preprocessing
from scipy import signal

# USAGE test.py [path to full video] [path to clip]
fullVideoPath = sys.argv[1]
clipPath = sys.argv[2]

# extract audio from video clips
fullVideo = VideoFileClip(fullVideoPath)
fullVideoAudio = fullVideo.audio

fullVideoDuration = fullVideo.duration

clip = VideoFileClip(clipPath)
clipAudio = clip.audio

# write audio to file
fullAudioPath = fullVideoPath.replace('csgo-clips', 'csgo-audio').replace('mp4', 'mp3')
clipAudioPath = clipPath.replace('csgo-clips', 'csgo-audio').replace('mp4', 'mp3')

# check if file exists before writing
if not os.path.isfile(fullAudioPath):
  fullVideoAudio.write_audiofile(fullAudioPath)

if not os.path.isfile(clipAudioPath):
  clipAudio.write_audiofile(clipAudioPath)

# extract audio with librosa
fullAudioLib, sampleRate = librosa.load(fullAudioPath)
clipAudioLib, sampleRate = librosa.load(clipAudioPath)

# count frames of each
fullAudioNumFrames = fullAudioLib.shape[0]
clipAudioNumFrames = clipAudioLib.shape[0]

a = signal.fftconvolve(fullAudioLib, clipAudioLib[::-1], mode='same')
print(a)
# calculate the time the clip occurs in the full video
# t = fullVideoDuration / fullAudioNumFrames * indexOfMax * 512

# print(t)
idx = np.argmax(a)
print(idx)
print(a.shape)
print(fullAudioLib.shape)

t = (idx/len(a)) * fullVideoDuration
print(t)o
plt.plot(a)
plt.show()


