import os.path
import librosa
import numpy as np
from numpy import save
from numpy import load
from scipy import signal
from scipy import stats


def getLibrosaPath(vidId):
  return "datastore/librosas/" + vidId + ".npy"


# retrieve librosa file from local
# takes filepath, returns numpy array
def loadLibrosa(filePath):
  data = load(filePath)
  sampleRate = int(data[-1])
  return (data[:-1], sampleRate)


# saves librosa file
def saveLibrosa(audio, sampleRate, targetPath):
  save(targetPath, np.append(audio, sampleRate))


# convert audio file to librosa file
def createLibrosa(audioFilePath):
  audio, sampleRate = librosa.load(audioFilePath)
  return (audio, sampleRate)


# check if librosa exists for a video
def librosaExists(filePath):
  return os.path.isfile(filePath)


def clipExistsInFull(clip, full):
  # run cros-correlation to find where clip occurs in full video
  correlation = signal.fftconvolve(full, clip[::-1], mode='same')
  # get index of max
  idx = np.argmax(correlation)
  # check for any spikes in correlation array
  z = np.abs(stats.zscore(correlation))
  spikes = np.where(z > 80) # 80 is a made up threshold
  hasMatch = np.isin(idx, spikes)
  return (hasMatch, idx)
