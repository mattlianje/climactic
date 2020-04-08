import librosa
import numpy as np
import helpers.librosaHelper as librosaHelper

def getAmp(audio, sampleRate, intervals):
  output = []
  
  # iterate intervals and calculate mfccs 
  for start, end in intervals:
    # splice full audio into clip
    clip = audio[start * sampleRate : end * sampleRate]
    amplitude = np.mean(clip)
    # add to output
    output.append(amplitude)
  
  return np.array(output)
