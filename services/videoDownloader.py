from pytube import YouTube
import os.path
from moviepy.editor import *

def getVideoPath(vidId):
  return "datastore/videos/" + vidId + ".mp4"


def getAudioPath(vidId):
  return "datastore/audio/" + vidId + ".wav"


def getVideoDuration(videoPath):
  video = VideoFileClip(videoPath)
  return video.duration


def downloadVid(vidUrl, vidId):
  fileName = vidId
  filePath = getVideoPath(vidId)

  if not os.path.isfile(filePath):
    print("Downloading ", vidUrl)
    YouTube(vidUrl).streams[0].download("datastore/videos/", fileName)
  else:
    print(vidUrl, " already downloaded")


def writeAudio(vidId):
  fileName = vidId + ".wav"
  filePath = getAudioPath(vidId)

  if not os.path.isfile(filePath):
    videoPath = getVideoPath(vidId)
    video = VideoFileClip(videoPath)
    audio = video.audio
    print("saving: ", fileName)
    audio.write_audiofile(filePath)
  else:
    print("Audio already exists")
