import librosa
import numpy as np
import helpers.librosaHelper as librosaHelper

def getMfcc(audio, sampleRate, intervals):
  output = []
  
  # iterate intervals and calculate mfccs 
  for start, end in intervals:
    # splice full audio into clip
    clip = audio[start * sampleRate : end * sampleRate]
    # extract mffcc
    mfcc = librosa.feature.mfcc(y=clip, sr=sampleRate, n_mfcc = 40)
    avgMfcc = np.mean(mfcc.T, axis=0)
    # convert to string
    mfccProcessed = np.array_str(avgMfcc)
    # add to output
    output.append(mfccProcessed)
  
  return np.array(output)
