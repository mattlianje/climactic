# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from os import path
from pydub import AudioSegment
from pocketsphinx import AudioFile
from SimpleAudioIndexer import SimpleAudioIndexer as sai
import youtube_dl
import pyaudio
import speech_recognition as sr
import pocketsphinx

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    # throw in the url of the video audio you want to grab as an mp3 here
    ydl.download(['https://www.youtube.com/watch?v=JZRXESV3R74'])

# TODO right now src is being hardcoded - be able to grab title from url in the future
src = "Donald Trump - The Art of the Insult-JZRXESV3R74.mp3"
dst = "test.wav"

# convert mp3 to wav for Sphinx speech to text                                                          
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "test.wav")
#other format examples
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

# use the audio file as the audio source

r = sr.Recognizer()
framerate = 10
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file
    decoder = r.recognize_sphinx(audio, show_all=True)
    print(decoder.seg())
    
    # Print out the entire transcript of the audio file
    # ------------------
    try:
        print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    # ------------------

    for seg in decoder.seg():
        print(seg.word, 'start time: ', seg.start_frame, ' | end time: ', seg.end_frame)

        # run a test where the word stupid gets saved as a new audio file in the current dir

        if (seg.word == 'stupid'):
            print('******', seg.word)
            t1 = (seg.start_frame -50) * framerate
            t2 = (seg.end_frame + 75) * framerate

            # Slice and export and new audio file with t1 and t2 being the bounds
            stupidAudio = AudioSegment.from_wav(AUDIO_FILE)
            stupidAudio = stupidAudio[t1:t2]
            stupidAudio.export('newStupid.wav', format='wav') # exports a wav to the current path
