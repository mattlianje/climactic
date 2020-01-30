from __future__ import unicode_literals
import youtube_dl
from os import path
from pydub import AudioSegment
import youtube_dl
import pyaudio
import speech_recognition as sr
import pocketsphinx
from scipy.io import wavfile
import wave
import matplotlib.pylab as plt
from textblob import TextBlob
import math
import sys
from aubio import source, pitch
import numpy as np
filepath = 'audio-files/'

ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'audio-files/%(title)s-%(id)s.%(ext)s'
        }

# TESTING = False

class videoObject:
    def __init__(self, url, isHighlight, isTest):
        self.url = url
        self.highlight = isHighlight
        self.isTest = isTest
        self.word_list = []
        self.amplitude_list = []
        self.pitch_list = []

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            self.info_dict = ydl.extract_info(self.url, download=False)

    def getTitle(self):
        video_title = self.info_dict.get('title', None)
        return video_title

    def getFilename(self):
        video_title = self.info_dict.get('title', None).replace(":", " -")
        video_filename = filepath + video_title + '-' + self.url.split("=", 1)[1] + '.mp3'
        return video_filename

    def getFilenameWav(self):
        video_title = self.info_dict.get('title', None)
        filename_wav = filepath + 'WAV-' + video_title + '-' + self.url.split("=", 1)[1] + '.wav'
        return filename_wav

    # Downloads mp3 from url and converts to wav
    def getAudio(self):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # Url of the youtube video - and the audio for that video will be downloaded as an mp3 in the current directory.
            ydl.download([self.url])

        dst = self.getFilenameWav()
        sound = AudioSegment.from_mp3(self.getFilename())
        sound.export(dst, format="wav")

    # Performs text analysis
    def getTextAnalysis(self):
        dst = self.getFilenameWav()
        # We can use .wav .aiff or .flac with this lib.
        AUDIO_FILE = dst
        # Uses AUDIO-FILE to do a speech to text.
        r = sr.Recognizer()
        framerate = 0.1
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file
            decoder = r.recognize_sphinx(audio, show_all=True)
            print(decoder.seg())

            # Prints out all the words and their start and end timestamps.
            for seg in decoder.seg():
                if (self.isTest == True):
                    print(seg.word, seg.start_frame, seg.end_frame)
                video_title = self.info_dict.get('title', None)
                word_dict = {
                                 'word': seg.word,
                                 'start_time_s': math.trunc(seg.start_frame/100),
                                 'end_time_s': math.trunc(seg.end_frame/100),
                                 'subjectivity': TextBlob(seg.word).sentiment.subjectivity,
                                 'polarity': TextBlob(seg.word).sentiment.polarity,
                                 'url': self.url,
                                 'video_title': video_title
                             }
                self.word_list.append(dict(word_dict))


    # Performs amplitude analysis
    def getAmplitudeAnalysis(self):

        obj = wave.open(self.getFilenameWav(), 'r')
        print("parameters:", obj.getparams())
        obj.close()

        fs, amp_data = wavfile.read(self.getFilenameWav()) #Frame rate and numpy array for amplitude at each frames
        nf = len(amp_data) # Number of frames

        duration = round((nf / fs), 0)
        print("Duration (in seconds):", duration)
        if duration <= 600:
            interval = 1
        elif duration <= 3600:
            interval = 5
        else:
            interval = 10

        # Variables for Amplitude parsing & Test dictionary for graphing amplitudes
        interval_amplitudes = {}

        fc, ic, c = 1, 1, 1 # frame counter (resets every interval), interval counter, and continuous frame countes
        amp_sum, max_amp, min_amp = 0, 0, 0 #amplitude sum, maximum amplitude, and minimum amplitude

        while c < nf:
            amp_sum += amp_data[c][0]
            if fc == (interval * fs) or c == nf-1:  # If you have gone through an interval

                # Calculate average amplitude in interval
                interval_avg = amp_sum / fc
                interval_amplitudes[ic] = interval_avg
                
                #print("Value: ", interval_avg, " FC: ", fc, " C: ", c)
                endtime = c/fs #Endtime = Counter / FrameRate
                #Dictionary for specific interval
                interval_dict = {
                                    'amplitude': interval_avg,
                                    'start_time_s': round(endtime - (fc/fs)),
                                    'end_time_s': round(endtime),
                                    'url': self.url
                                }

                # Find Max and Min Amplitudes for reference
                if interval_avg >= max_amp:
                    max_amp = interval_avg
                elif interval_avg <= min_amp:
                    min_amp = interval_avg

                # Reset all counters
                fc = 0
                amp_sum = 0
                ic += 1

                #Append to Video Object Amplitude List
                self.amplitude_list.append(dict(interval_dict))

            fc += 1
            c += 1


        #If testing, loop through interval_amplitudes intervals and outputs them
        if (self.isTest == True):
            for x, y in interval_amplitudes.items():
                print(x, y)

            print('Max Amplitude: ', max_amp)
            print('Min Amplitude: ', min_amp)
            print('Length of Array: ', nf)
            # We must sort the dictionary to be able to iterate through it.
            plt.plot(*zip(*sorted(interval_amplitudes.items())))
            plt.show()

    def getPitchAnalysis(self):
        # VARIABLES SETUP
        fc, ic, c = 1, 1, 1 # frame counter (resets every interval), interval counter, continuous frame count
        pitch_sum, co_sum, max_pitch, min_pitch = 0, 0, 0, 0 #pitch sum, confidence sum, maximum pitch, and minimum pitch

        interval_pitches = {}

        win_s = 4096 # fft size
        hop_s = 512 # hop size
        
        fs, audio_data = wavfile.read(self.getFilenameWav()) # Get Frame Rate and audio data
        nf = len(audio_data) # Number of frames
        duration = round((nf / fs), 0) #Duration of video in seconds
        
        if duration <= 600:
            interval = 1
        elif duration <= 3600:
            interval = 5
        else:
            interval = 10

        source_file = source(self.getFilenameWav(), fs, hop_s)
        fs = source_file.samplerate

        tolerance = 0.8

        pitch_o = pitch("yin", win_s, hop_s, fs)
        pitch_o.set_unit("midi")
        pitch_o.set_tolerance(tolerance)

        pitch_data = []
        confidence_data = []

        hop_c = 0 # Hop Counter
        index_c = 1 # Index Counter
        
        while c <= nf:
            while fc <= interval*fs:
                samples, read = source_file()
                frame_pitch = pitch_o(samples)[0]
                pitch_data += [frame_pitch]
                pitch_sum += frame_pitch # Using this sum to average out over interval
                confidence = pitch_o.get_confidence()
                confidence_data += [confidence]
                co_sum += confidence

                fc += read
                c += read
                hop_c += 1

                if read < hop_s: break
            
            # Calculate average frequency in interval
            interval_avg_p = pitch_sum / hop_c
            interval_avg_c = co_sum / hop_c
            interval_pitches[ic] = interval_avg_p

            #print("Hop Count: ", hop_c, " Value: ", interval_avg_p, " FC: ", fc, " C: ", c)
            
            endtime = c/fs #Endtime = Counter / FrameRate
            #Dictionary for specific interval
            interval_dict = {
                                'pitch': interval_avg_p,
                                'p_confidence': interval_avg_c,
                                'start_time_s': round(endtime - (fc/fs)),
                                'end_time_s': round(endtime),
                                'url': self.url
                            }

            # Find Max and Min Frequency for reference
            if interval_avg_p >= max_pitch:
                max_pitch = interval_avg_p
            elif interval_avg_p <= min_pitch:
                min_pitch = interval_avg_p

            # Reset all counters and variables
            fc = 0
            ic += 1
            pitch_sum = 0
            hop_c = 0
            c = index_c*fs
            index_c += 1

            #Append to Video Object Pitch List
            self.pitch_list.append(dict(interval_dict))

        if (self.isTest == True):
            print("Duration (From Pitch Analysis): ", duration)
            for x, y in interval_pitches.items():
                print(x, y)

            print('Max Pitch: ', max_pitch)
            print('Min Pitch: ', min_pitch)

            # We must sort the dictionary to be able to iterate through it.
            plt.plot(pitch_data)
            plt.show()
            plt.plot(*zip(*sorted(interval_pitches.items())))
            plt.show()


