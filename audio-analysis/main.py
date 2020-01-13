import videoHelper

trumpVideo = videoHelper.videoObject('https://www.youtube.com/watch?v=JZRXESV3R74', False)
print(trumpVideo.getFilename())
trumpVideo.getAudio()
trumpVideo.getTextAnalysis()
trumpVideo.getAmplitudeAnalysis()






