import videoHelper
import pandas as pd

trumpVideo = videoHelper.videoObject('https://www.youtube.com/watch?v=JZRXESV3R74', False)
print(trumpVideo.getFilename())
trumpVideo.getAudio()
trumpVideo.getTextAnalysis()
trumpVideo.getAmplitudeAnalysis()

df = pd.DataFrame(trumpVideo.word_list)
print(df)