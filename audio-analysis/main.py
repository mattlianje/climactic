import videoHelper
import pandas as pd

TESTING = False #Define if you are testing or not. Make sure to check videoHelper.py for testing too

# Save Video function creates a video object and outputs all the nice analysis stuff
# Will add a function to consolidate video data into a dictionary 
# Will add a function to push video dictionaries to SQL table
def saveVideo(url, tag):
    video = videoHelper.videoObject(url, tag)
    print(video.getFilename())
    video.getAudio()
    video.getTextAnalysis()
    video.getAmplitudeAnalysis()

    if (TESTING):
        df1 = pd.DataFrame(video.word_list) 
        df2 = pd.DataFrame(video.amplitude_list) 
        print(df1)
        print(df2)
    

##### Prompt for Highlight Video and Tagging #####
answer = input("Option 1. single | Option 2. csv | Option 3. test \n")

#If user wants to upload only a single video
if answer == 'single' or answer == '1':
    url = input("Provide YT Link: ")
    tag = input("Provide highlight tag (True/False): ")
    print("Link: ", url)
    print("Tag: ", tag)
    saveVideo(url, tag)
#If user wants to upload only a CSV of videos
elif answer == 'csv' or answer == '2':
    inputCSV = input("Provide csv with file and path \n")
    tuplesDF = pd.read_csv(inputCSV)
    print(tuplesDF.head())
    i = 0
    while i < len(tuplesDF.index):
        print("\n For Video #", i+1, ":")
        url = tuplesDF.loc[i, 'YT_LINK']
        tag = tuplesDF.loc[i, 'H_TAG']
        print("Link: ", url, " | Tag: ", tag)
        saveVideo(url, tag)
        i += 1
        print("\n --------------------------------")
elif answer == 'test' or answer == '3':
    saveVideo("https://www.youtube.com/watch?v=JZRXESV3R74", True)