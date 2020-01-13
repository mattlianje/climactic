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

ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

class videoObject:
    def __init__(self, url, isHighlight):
        self.url = url
        self.highlight = isHighlight

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            self.info_dict = ydl.extract_info(self.url, download=False)

    def getTitle(self):
        video_title = self.info_dict.get('title', None)
        return video_title

    def getFilename(self):
        video_title = self.info_dict.get('title', None).replace(":", " -")
        video_filename = video_title + '-' + self.url.split("=", 1)[1] + '.mp3'
        return video_filename

    def getFilenameWav(self):
        video_title = self.info_dict.get('title', None)
        filename_wav = 'WAV-' + video_title + '-' + self.url.split("=", 1)[1] + '.wav'
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
        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), dst)

        # Uses AUDIO-FILE to do a speech to text.
        r = sr.Recognizer()
        framerate = 0.1
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file
            decoder = r.recognize_sphinx(audio, show_all=True)
            print(decoder.seg())

            # Prints out all the words and their start and end timestamps.
            for seg in decoder.seg():
                print(seg.word, seg.start_frame, seg.end_frame)

                # Run a test where the word stupid gets saved as a new audio file.
                if (seg.word == 'stupid'):
                    print('******', seg.word)
                    print('******', seg.start_frame, seg.end_frame)
                    t1 = (seg.start_frame - 50) * 10
                    t2 = (seg.end_frame + 300) * 10

                    stupidAudio = AudioSegment.from_wav(AUDIO_FILE)
                    stupidAudio = stupidAudio[t1:t2]
                    stupidAudio.export('newStupid.wav', format='wav')  # exports a wav to the current path

    # Performs amplitude analysis
    def getAmplitudeAnalysis(self):

        obj = wave.open(self.getFilenameWav(), 'r')
        print("parameters:", obj.getparams())
        obj.close()

        fs, amp_data = wavfile.read(self.getFilenameWav())
        nf = len(amp_data)

        duration = round((nf / fs), 0)
        print("Duration (in seconds):", duration)
        if duration <= 600:
            interval = 1
        elif duration <= 3600:
            interval = 5
        else:
            interval = 10

        # Variables for Amplitude parsing
        interval_amplitudes = {}

        # Test dictionary for graphing amplitudes
        raw_amplitudes = {}

        fc, ic, fc_continuous = 1, 1, 1
        amp_sum, max_amp, min_amp = 0, 0, 0

        for c in range(len(amp_data)):
            amp_sum += amp_data[c][0]
            if fc == (interval * fs) or c == len(amp_data):  # If you have gone through an interval

                # Calculate average amplitude in interval
                interval_avg = amp_sum / fc
                interval_amplitudes[ic] = interval_avg

                #Dictionary for specific interval
                interval_dict = {   'amplitude': interval_avg,
                                    'start_time_ms': ((fc_continuous/fs) - interval),
                                    'end_time_ms': (fc_continuous/fs),
                                    'url': self.url
                                }

                raw_amplitudes[ic] = interval_avg

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
            fc_continuous += 1

        #Commented out but decided to keep in case, loop through interval_amplitudes intervals and outputs them
        #for x, y in interval_amplitudes.items():
        #    print(x, y)

        print('Max Amplitude: ', max_amp)
        print('Min Amplitude: ', min_amp)

        # We must sort the dictionary to be able to iterate through it.
        plt.plot(*zip(*sorted(raw_amplitudes.items())))
        plt.show()

