# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import youtube_dl
import wave
import scipy
import numpy as np
from scipy.io import wavfile
import wave

filename = 'JRE-CDG.wav'

obj = wave.open(filename,'r')
#print( "Number of channels",obj.getnchannels())
#print ( "Sample width",obj.getsampwidth())
#print ( "Frame rate.",obj.getframerate())
#print ("Number of frames",obj.getnframes())
print ( "parameters:",obj.getparams())
obj.close()

fs, amp_data = wavfile.read(filename)
nf = len(amp_data)

duration = round((nf / fs), 0)
print( "Duration (in seconds):", duration)

# Determine interval length based on audio length
# Basically,
# If video <= 10 minutes, Interval = 1 second
# If video > 10 minutes AND <= 1 hour, Interval = 5 seconds
# If video > 1 hour, Interval = 10 seconds

if duration <= 600:
    interval = 1
elif duration <= 3600:
    interval = 5
else:
    interval = 10

#Variables for Amplitude parsing
interval_amplitudes= {}
fc = 1
ic = 1
amp_sum = 0
max_amp = 0
min_amp = 0

for c in range(len(amp_data)):
    amp_sum += amp_data[c][0]
    if fc == (interval*fs) or c == len(amp_data): #If you have gone through an interval

        #Calculate average amplitude in interval
        interval_avg = amp_sum/fc
        interval_amplitudes['Interval', ic] = interval_avg

        #Find Max and Min Amplitudes for reference
        if interval_avg >= max_amp:
            max_amp = interval_avg
        elif interval_avg <= min_amp:
            min_amp = interval_avg

        #Reset all counters
        fc = 0
        amp_sum = 0
        ic += 1
    fc += 1

for x, y in interval_amplitudes.items():
  print(x, y)

print('Max Amplitude: ', max_amp)
print('Min Amplitude: ', min_amp)