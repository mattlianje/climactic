import os.path
import librosa
import numpy as np
from numpy import save
from numpy import load

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


# convert audio file to librosa file and save it
def createLibrosa(audioFilePath):
  audio, sampleRate = librosa.load(audioFilePath)
  return (audio, sampleRate)


# check if librosa exists for a video
def librosaExists(filePath):
  return os.path.isfile(filePath)
