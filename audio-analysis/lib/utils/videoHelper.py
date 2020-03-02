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
import librosa
from librosa import display

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
    def __init__(self, url, windowSize, overlap, isHighlight, isTest):
        self.url = url
        self.windowSize = windowSize
        self.overlap = overlap
        self.highlight = isHighlight
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
        video_filename = filepath + video_title + '-' + self.url.split("=", 1)[1] + '.mp3'
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
            decoded_words = decoder.seg()
            video_title = self.info_dict.get('title', None)
            # Number of seconds to move window forward by at each iteration of this sliding window.
            slide_inc = self.windowSize - self.overlap
            if self.overlap > self.windowSize:
                raise Exception('ERROR - overlap must not exceed windowSize.')
            num_windows = self.getNumberOfWindows()
            print(decoder.seg())

            for i in range(0, num_windows):
                # Current window start time in s.
                curr_win_start = i * slide_inc
                # Current window end time  in s.
                curr_win_end = (i * slide_inc) + self.windowSize
                # Current window lists for word, subjectivity, and polarity
                curr_win_pol_list, curr_win_sbj_list, curr_win_words = ([] for i in range (3))
                # Handling the fencepost case.
                if curr_win_start > (self.getDuration() - self.windowSize):
                    curr_win_end = self.getDuration()
                for seg in decoded_words:
                    if (self.isTest == True):
                        print(seg.word, seg.start_frame, seg.end_frame)
                    # Current word start time in s.
                    curr_word_start = math.trunc(seg.start_frame/100)
                    if curr_win_start <= curr_word_start < curr_win_end:
                        curr_win_pol_list.append(TextBlob(seg.word).sentiment.polarity)
                        curr_win_sbj_list.append(TextBlob(seg.word).sentiment.subjectivity)
                        curr_win_words.append(seg.word)
                pol_avg = average(curr_win_pol_list)
                subj_avg = average(curr_win_sbj_list)
                word_list_to_string = ' '.join(map(str, curr_win_words))

                segment_dict = {
                                 'word': word_list_to_string,
                                 'start_time_s': curr_win_start,
                                 'end_time_s': curr_win_end,
                                 'subjectivity': subj_avg,
                                 'polarity': pol_avg,
                                 'url': self.url,
                                 'video_title': video_title
                               }
                self.word_list.append(dict(segment_dict))

    def getPitchAnalysis(self):
        # VARIABLES SETUP
        fc, ic, c = 1, 1, 1 # frame counter (resets every interval), interval counter, continuous frame count
        pitch_sum, co_sum = 0, 0 #pitch sum, confidence sum, maximum pitch, and minimum pitch
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
        print("\n", source_file, "\n")
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

            
            endtime = c/fs #Endtime = Counter / FrameRate
            pitch_dict = {
                                'pitch': interval_avg_p,
                                'p_confidence': interval_avg_c,
                                'start_time_s': round(endtime - (fc/fs)),
                                'end_time_s': round(endtime),
                                'url': self.url
                            }

            #Debugging
            if (self.isTest):
                print("Pitch: ", interval_avg_p, " P_Confidence: ", interval_avg_c)

            # Reset all counters and variables
            fc = 0
            ic += 1
            pitch_sum = 0
            hop_c = 0
            c = index_c*fs
            index_c += 1

            #Append to Video Object Pitch List
            self.pitch_list.append(dict(pitch_dict))

        if (self.isTest):
            amplitude_data = [d.get('amplitude') for d in self.amplitude_list]
            plt.plot(amplitude_data)
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
        if duration <= 600:
            interval = 1
        elif duration <= 3600:
            interval = 5
        else:
            interval = 10
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
                    print("Interval: ", ic, " FC: ", fc, " C: ", c, " CS: ", cs,)
                    print("Audio: ", interval_amp_avg, "MFCC(1): ", mfccs_processed[0])

                # Reset all counters
                fc = 0
                ic += 1
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


