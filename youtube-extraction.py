# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from os import path
from pydub import AudioSegment
# from pocketsphinx import AudioFile
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

src = "Donald Trump - The Art of the Insult-JZRXESV3R74.mp3"
dst = "test.wav"

# convert wav to mp3                                                            
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "test.wav")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")

# use the audio file as the audio source
r = sr.Recognizer()
framerate = 0.1
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file
    decoder = r.recognize_sphinx(audio, show_all=True)
    print(decoder.seg())
    #print(decoder)
    # for seg in decoder.seg():
    #     print(seg)
    # print ([(seg.word, seg.start_frame/framerate) for seg in decoder.seg()])
    for seg in decoder.seg():
        print(seg.word, seg.start_frame, seg.end_frame)

        # run a test where the word stupid gets saved as a new audio file

        if (seg.word == 'stupid'):
            print('******', seg.word)
            print('******', seg.start_frame, seg.end_frame)
            t1 = (seg.start_frame) * 10
            t2 = (seg.end_frame + 3000) * 10

            stupidAudio = AudioSegment.from_wav(AUDIO_FILE)
            stupidAudio = stupidAudio[t1:t2]
            stupidAudio.export('newStupid.wav', format='wav') # exports a wav to the current path

# recognize speech using Sphinx
# ------------------
# try:
#     print("Sphinx thinks you said " + r.recognize_sphinx(audio))
# except sr.UnknownValueError:
#     print("Sphinx could not understand audio")
# except sr.RequestError as e:
#     print("Sphinx error; {0}".format(e))
# -----------------


# indexer = sai(mode="cmu", src_dir="C:/Users/matth/OneDrive/4A/MSCI 401/gregarious-wolf")
# indexer.index_audio()
# print(indexer.get_timestamps())

# Frames per Second
# fps = 100

# audio1 = sr.AudioFile(AUDIO_FILE)

# for phrase in audio1:  # frate (default=100)
#     print('-' * 28)
#     print('| %5s |  %3s  |   %4s   |' % ('start', 'end', 'word'))
#     print('-' * 28)
#     for s in phrase.seg():
#         print('| %4ss | %4ss | %8s |' % (s.start_frame / fps, s.end_frame / fps, s.word))
#     print('-' * 28)