import librosa
import numpy as np
from numpy import save
from numpy import load
from scipy import signal
from scipy import stats
import os.path

# retrieve librosa file from local
def retrieveLibrosa(filePath):
  data = load(filePath)
  sampleRate = int(data[-1])
  return (data[:-1], sampleRate)

# convert audio file to librosa file and save it
def createAndSaveLibrosa(audioFilePath, targetPath):
  audio, sampleRate = librosa.load(audioFilePath)
  # save librosa
  save(targetPath, np.append(audio, sampleRate))
  return (audio, sampleRate)

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

# check if librosa file already exists, otherwise convert
def extractLibrosa(audioFilePath, savePath):
  if os.path.isfile(savePath):
    audio, sampleRate = retrieveLibrosa(savePath)
  else: # convert audio file to librosa
    audio, sampleRate = createAndSaveLibrosa(audioFilePath, savePath)
  return (audio, sampleRate)

