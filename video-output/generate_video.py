from moviepy.editor import *
import json

with open("../demofile-parsing/timestamps.json", "r") as read_file:
    data = json.load(read_file)

fullvideo = VideoFileClip("/Users/tylerlam/Downloads/CSGO - Liquid vs. mousesports [Cache] Map 1 - GRAND FINAL - ESL One New York 2018.mp4")

clips = []
roundNumber = 1
for round in data:
  transition = TextClip("Round {}".format(roundNumber), font='Arial', fontsize=70, color="white", size=fullvideo.size)
  roundNumber += 1
  clips.append(transition.set_duration(3))
  for highlight in round:
    start_time = highlight[0]
    end_time = highlight[1]
    clips.append(fullvideo.subclip(start_time, end_time))

final_video = concatenate_videoclips(clips)
final_video.write_videofile("highlights.mp4", codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
