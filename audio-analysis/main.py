import videoHelper
import pandas as pd

# Save Video function creates a video object and outputs all the nice analysis stuff
# Will add a function to consolidate video data into a dictionary 
# Will add a function to push video dictionaries to SQL table
def saveVideo(ytURL, hTag):
    videoX = videoHelper.videoObject(ytURL, hTag)
    print(videoX.getFilename())
    videoX.getAudio()
    videoX.getTextAnalysis()
    videoX.getAmplitudeAnalysis()

##### Prompt for Highlight Video and Tagging #####
answer = input("Are you entering a single video (enter 'single') or CSV (enter 'csv') \n")

#If user wants to upload only a single video
if answer == 'single':
    ytURL = input("Provide YT Link: ")
    hTag = input("Provide highlight tag (True/False): ")
    print("Link: ", ytURL)
    print("Tag: ", hTag)
    saveVideo(ytURL, hTag) #Call 
#If user wants to upload only a CSV of videos
elif answer == 'csv':
    inputCSV = input("Provide csv with file and path \n")
    tuplesDF = pd.read_csv(inputCSV)
    print(tuplesDF.head())
    i = 0
    while i < len(tuplesDF.index):
        print("\n For Video #", i+1, ":")
        ytURL = tuplesDF.loc[i, 'YT_LINK']
        hTag = tuplesDF.loc[i, 'H_TAG']
        print("Link: ", ytURL, " | Tag: ", hTag)
        saveVideo(ytURL, hTag)
        i += 1
        print("\n --------------------------------")






