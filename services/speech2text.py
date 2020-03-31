import speech_recognition as sr
from scipy.io import wavfile
import pandas as pd
from tqdm import tqdm
from textblob import TextBlob
import os
import sys

def getText(audioPath, intervals):
    r = sr.Recognizer()
    #raw_file = wavfile.read(audioPath)
    file = sr.AudioFile(audioPath)
    video_title = ''
    word_list = []

    for interval in tqdm(intervals):
        window_start = interval[0]
        window_end = interval[1]
        window_duration = window_end - window_start
        with file as source:
            audio = r.record(source, offset=window_start, duration=window_duration)
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
            'subjectivity': subj_avg,
            'polarity': pol_avg,
        }
        word_list.append(dict(segment_dict))
    return pd.DataFrame(word_list)

def average(inputList):
    avg = 0
    if len(inputList) != 0:
        avg = sum(inputList) / len(inputList)
    return avg

