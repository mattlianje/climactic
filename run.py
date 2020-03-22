import sys
import pandas as pd
import services.videoDownloader as videoDownloader
import services.createIntervals as intervalCreator
import helpers.librosaHelper as librosaHelper
import helpers.dbHelper as dbHelper

# This is the commander, it will string together all the services 
# INPUT: youtube url
# USAGE: python run.py [youtube url]

# Get YT url
vidUrl = sys.argv[1]

# If no url provided exit
if not vidUrl:
  print('Please enter a youtube video url')
  exit()

# get video id, we will use the video id as the name for all files generated
vidId = vidUrl.replace('https://www.youtube.com/watch?v=', '')

# Download youtube video
videoPath = videoDownloader.getVideoPath(vidId)
videoDownloader.downloadVid(vidUrl, vidId)

# Save audio
audioPath = videoDownloader.getAudioPath(vidId)
videoDownloader.writeAudio(vidId)

# Get the length of the video
vidDuration = int(videoDownloader.getVideoDuration(videoPath))

# # Create 4 second intervals
INTERVAL_LENGTH = 4
OVERLAP_LENGTH = 2

# Get intervals -> [[start, end], [start, end]]
intervals = intervalCreator.getIntervals(vidDuration, INTERVAL_LENGTH, OVERLAP_LENGTH)
# insert intervals into db
intervalCreator.insertIntervals(vidUrl, intervals)

# Generate and save as librosa
print("Generating librosa")
librosaPath = librosaHelper.getLibrosaPath(vidId)

if not librosaHelper.librosaExists(librosaPath):
  audio, sampleRate = librosaHelper.createLibrosa(audioPath)
  librosaHelper.saveLibrosa(audio, sampleRate, librosaPath)

# Feature extraction

