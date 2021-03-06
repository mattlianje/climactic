from __future__ import unicode_literals
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
import librosa
from tqdm import tqdm
from librosa import display

filepath = 'audio-files/'

ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'outtmpl': 'audio-files/%(title)s-%(id)s.%(ext)s'
        }

# TESTING = False

class videoObject:
    def __init__(self, url, windowSize, overlap, isTest):
        self.url = url
        self.windowSize = windowSize
        self.overlap = overlap
        self.isTest = isTest
        self.word_list = []
        self.amplitude_list = []
        self.pitch_list = []
        self.mfcc_list = []

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            self.info_dict = ydl.extract_info(self.url, download=False)
            # video_title = self.info_dict.get('title', None)

    # Returns the video duration in seconds.
    def getDuration(self):
        video_title = self.info_dict.get('duration', None)
        return video_title

    def getNumberOfWindows(self):
        num_windows = self.getDuration() // (self.windowSize - self.overlap)
        return num_windows

    def getTitle(self):
        video_title = self.info_dict.get('title', None)
        return video_title

    def getFilename(self):
        video_title = self.info_dict.get('title', None).replace(":", " -")
        video_filename = filepath + video_title + '-' + self.url.split("=", 1)[1] + '.wav'
        return video_filename

    def getFilenameWav(self):
        video_title = self.info_dict.get('title', None)
        filename_wav = filepath + 'WAV-' + video_title + '-' + self.url.split("=", 1)[1] + '.wav'
        return filename_wav
    
    # Downloads mp3 from url and converts to wav
    def getAudio(self):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # Url of the youtube video - and the audio directory.
            ydl.download([self.url])



    # Performs text analysis
    def getTextAnalysis(self):
        if self.overlap > self.windowSize:
            raise Exception('ERROR - overlap must not exceed windowSize.')
        r = sr.Recognizer()
        # We can use .wav .aiff or .flac with this lib.
        raw_file = self.getFilename()
        file = sr.AudioFile(raw_file)
        video_title = self.info_dict.get('title', None)
        num_windows = self.getNumberOfWindows()
        slide_inc = self.windowSize - self.overlap

        for window in tqdm(range(num_windows)):
            window_start = window * slide_inc
            window_end = window_start + self.windowSize
            with file as source:
                audio = r.record(source, offset=window_start, duration=self.windowSize)
                payload = r.recognize_google(audio, show_all=True)
                # Lists for temp storage of words and their sentiment scores
                curr_win_pol_list, curr_win_sbj_list, curr_win_words = ([] for i in range(3))
                # Initialize phrase to null ... 'silent' speech
                phrase = None
                if len(payload) != 0:
                    phrase = payload['alternative'][0]['transcript']
                    if phrase != None:
                        for word in phrase.split():
                            curr_win_pol_list.append(TextBlob(word).sentiment.polarity)
                            curr_win_sbj_list.append(TextBlob(word).sentiment.subjectivity)
                            curr_win_words.append(word)
                pol_avg = average(curr_win_pol_list)
                subj_avg = average(curr_win_sbj_list)

            segment_dict = {
                'word': phrase,
                'start_time_s': window_start,
                'end_time_s': window_end,
                'subjectivity': subj_avg,
                'polarity': pol_avg,
                'url': self.url,
                'video_title': video_title
            }
            self.word_list.append(dict(segment_dict))

    def getPitchAnalysis(self, start_end_df):
        # VARIABLES SETUP
        fc, ic, c = 1, 1, 1 # frame counter (resets every interval), interval counter, continuous frame count
        pitch_sum, co_sum = 0, 0 #pitch sum, confidence sum, maximum pitch, and minimum pitch
        win_s = 4096 # fft size
        hop_s = 512 # hop size
        fs, audio_data = wavfile.read(self.getFilename()) # Get Frame Rate and audio data
        nf = len(audio_data) # Number of frames
        duration = round((nf / fs), 0) #Duration of video in seconds
        interval = 4 # Interval in seconds
        source_file = source(self.getFilename(), fs, hop_s)
        print("\n", source_file, "\n")
        fs = source_file.samplerate
        tolerance = 0.8
        pitch_o = pitch("yin", win_s, hop_s, fs)
        pitch_o.set_unit("midi")
        pitch_o.set_tolerance(tolerance)
        pitch_data = []
        hop_c = 0 # Hop Counter
        index_c = interval # Index Counter
        print('FS: ', fs)
        print('Getting Pitch For each hop..')
        while c <= nf:
            while fc <= interval*fs:
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
            index_c += interval  

        i = 0
        while i < len(start_end_df.index):
            starttime = start_end_df.loc[i, 'start']
            endtime = start_end_df.loc[i, 'end']
            # Calculate average frequency in interval
            startinterval = math.trunc(round((starttime*fs)/hop_s))
            endinterval = math.trunc(round((endtime*fs)/hop_s))
            if endinterval > len(pitch_data)-1: endinterval = len(pitch_data)-1
            hop_c = endinterval - startinterval
            for _p in pitch_data[startinterval:endinterval]:
                pitch_sum += _p

            interval_avg_p = pitch_sum / hop_c
            pitch_dict = {
                        'pitch': interval_avg_p,
                        'start_time_s': round(starttime),
                        'end_time_s': round(endtime),
                        'url': self.url
                        }
            #Debugging
            if (self.isTest):
                print("Interval: ", i+1, " FC: ", fc, " C: ", c, "IndexC: ", index_c, "HopC: ", hop_c, "StartTime: ", starttime, "EndTime: ", endtime)
                print("Start Interval:", startinterval, "End Interval:", endinterval)
                print("Pitch Sum: ", pitch_sum)
                print("Array Length: ", len(pitch_data), "Begin Array: ", pitch_data[startinterval], "End Array: ", pitch_data[endinterval])
                print("Pitch: ", interval_avg_p)
                print()
            
            #Append to Video Object Pitch List
            self.pitch_list.append(dict(pitch_dict))

            #Increment and Reset Variables
            i+=1
            pitch_sum=0
        

        if (self.isTest):
            print("C Total: ", c)
            pitch_data = [d.get('pitch') for d in self.pitch_list]
            plt.plot(pitch_data)
            plt.show()



    def getAmpMFCCAnalysis(self):
        ##################################
        #
        #        Variables Setup
        #
        ##################################
        
        ######## Global Variables ########
        uselibrosa = True
        # Frame rate and numpy array for audio at each frames
        if uselibrosa:
            audio_data, fs = librosa.load(self.getFilenameWav())
        else:
            fs, audio_data = wavfile.read(self.getFilenameWav())  
        nf = len(audio_data) # Number of frames
        duration = round((nf / fs), 0) #Duration in secodns
        interval = 4 # Interval in seconds
        interval_overlap = 2 # Interval overlap in seconds
        ic, c, fc, cs = 1, 1, 1, 1 # interval counter, continuous frame counter, frame counter (resets every interval)
        
        ######## Declaration of Audio Info ########
        print('')
        print("Duration (in seconds):", duration, "| (in frames): ", nf)
        print('Audio file min~max range: {0:.2f} to {0:.2f}'.format(np.min(audio_data), np.max(audio_data)))
        print('')

        ##################################
        #
        #       Audio Analysis (Loop)
        #
        ##################################

        while c < nf:
            if fc == (interval * fs) or c == nf-1: # For each interval, extract the features
                interval_audio_data = audio_data[cs:c]
                start_time = (cs-1)/fs
                end_time = c/fs
                
                # Amplitude
                interval_amp_avg = sum(interval_audio_data) / fc
                amp_dict = {
                            'amplitude': interval_amp_avg,
                            'start_time_s': round(start_time),
                            'end_time_s': round(end_time),
                            'url': self.url
                            }
                
                # MFCCs
                mfccs = librosa.feature.mfcc(y=interval_audio_data, sr=fs, n_mfcc = 40)
                mfccs_processed = np.mean(mfccs.T,axis=0)
                mfcc_dict = {
                            'start_time_s': round(start_time),
                            'end_time_s': round(end_time),
                            'url': self.url
                            }
                x = 0
                while x < len(mfccs_processed):
                    #print(mfccs_processed[x])
                    mfcc_dict['mfcc_' + str(x+1)] = mfccs_processed[x]
                    x += 1

                #Append to Video Object Lists
                self.amplitude_list.append(dict(amp_dict))
                self.mfcc_list.append(dict(mfcc_dict))

                # Debugging - Printing out values
                if(self.isTest):
                    print("Interval: ", ic, " FC: ", fc, " C: ", c, " CS: ", cs, "StartTime: ", start_time, "EndTime: ", end_time)
                    print("Audio: ", interval_amp_avg, "MFCC(1): ", mfccs_processed[0])

                # Reset all counters
                fc = 0
                ic += 1
                if c < nf-1: c = c - (interval_overlap*fs)
                cs = c + 1
                    
            # Increment through Audio    
            c += 1
            fc += 1


        # Print out graphs
        if(self.isTest):
            amplitude_data = [d.get('amplitude') for d in self.amplitude_list]
            plt.plot(amplitude_data)
            plt.show()
            
def average(inputList):
    avg = 0
    if len(inputList) != 0:
        avg = sum(inputList) / len(inputList)
    return avg


