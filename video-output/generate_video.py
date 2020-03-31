from moviepy.editor import *
import numpy as np
import json
import sys

# USAGE python generate_video.py [path to full video] [path to highlight timestamps] [output filename]
pathToFullVideo = sys.argv[1]
pathToTimestamps = sys.argv[2]
outputFilename = sys.argv[3] or "highlights.mp4"

npzfile = np.load(pathToTimestamps)
data = npzfile['rf_timestamps']

fullvideo = VideoFileClip(pathToFullVideo)

clips = []
for start_time, end_time in data:
  clips.append(fullvideo.subclip(start_time, end_time))

final_video = concatenate_videoclips(clips)
final_video.write_videofile("highlight-videos/" + outputFilename, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
