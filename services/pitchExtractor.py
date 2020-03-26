import numpy as np
import math
import wave
import sys
from aubio import source, pitch
from scipy.io import wavfile

def getPitch(audioPath, intervals):
  # VARIABLES SETUP
  fc, ic, c = 1, 1, 1 # frame counter (resets every interval), interval counter, continuous frame count
  pitch_sum = 0 #pitch sum, confidence sum, maximum pitch, and minimum pitch
  win_s, hop_s = 4096, 512 # fft size, hop size
  fs, audio_data = wavfile.read(audioPath) # Get Frame Rate and audio data
  nf = len(audio_data) # Number of frames
  source_file = source(audioPath, 44100, hop_s)
  fs = source_file.samplerate
  tolerance = 0.8
  pitch_o = pitch("yin", win_s, hop_s, fs)
  pitch_o.set_unit("midi")
  pitch_o.set_tolerance(tolerance)
  pitch_data = []
  hop_c = 0 # Hop Counter
  index_c = 4 # Index Counter - 4 seconds per intervals

  while c <= nf:
    while fc <= 4*fs:
        samples, read = source_file()
        frame_pitch = pitch_o(samples)[0]
        pitch_data += [frame_pitch]
        fc += read
        c += read

        if read < hop_s: break

    # Reset all counters and variables
    fc = 0
    ic += 1
    c = index_c*fs
    index_c += 4  

  i = 0
  output = []
  for start_end in intervals:
    starttime = start_end[0]
    endtime = start_end[1]
    # Calculate average frequency in interval
    startinterval = math.trunc(round((starttime*fs)/hop_s))
    endinterval = math.trunc(round((endtime*fs)/hop_s))
    if endinterval > len(pitch_data)-1: endinterval = len(pitch_data)-1
    hop_c = endinterval - startinterval
    for _p in pitch_data[startinterval:endinterval]:
        pitch_sum += _p

    interval_pitch = pitch_sum / hop_c
    output.append(interval_pitch)

    #Increment and Reset Variables
    i+=1
    pitch_sum=0
  
  return np.array(output)
