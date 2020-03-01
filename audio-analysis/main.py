import pandas as pd
import sys
import os
import lib.etl.dfHelper as dfHelper
import lib.utils.videoHelper as videoHelper
from lib.etl.sqlConnection import sqlConnectionSetup, urlExists, getEngine

# Run unit tests first
os.system('python test.py -v')

# Pass `python main.py log` as optional arg to see print statements
TESTING = False
if len(sys.argv) == 2:
    if sys.argv[1] == 'log':
        TESTING = True

# Using this Trump Video for testing
trump_video = "https://www.youtube.com/watch?v=JZRXESV3R74"

engine = getEngine(TESTING)

# analyzeVideoSound creates a video object and outputs all the nice analysis stuff ...
# inputs:
# url <- YouTube url of video to extract audio from
# tag <- True if video is highlight, else False
#
# outputs:
# Summary statistics wip ...
 
def analyzeVideoSound(url, tag):
    global engine
    global TESTING
    # Size of sliding window in seconds to partition video by.
    window_size = 4
    video = videoHelper.videoObject(url, window_size, tag, TESTING)
    print(video.getFilename())
    video.getAudio()
    video.getTextAnalysis()
    video.getAmpMFCCAnalysis()
    video.getPitchAnalysis()

    #    df1              df2                df4                |
    # (time, word)   (time, amplitude)   (time, pitch)          |
    #     |                |                  |                 |  
    #     |                |                  |                 |
    #     V________________V                  |                 |
    #            |                            |                 |
    #            |                            |                 |
    #            V____________________________V                 |
    #           df3                |                            |
    #   (word, time, amplitude)    |                            |
    #                              |                            |
    #                              V                            V
    #                             df5                           df6
    #                 (word, time, amplitude, pitch)          (mfcc)

    df1 = pd.DataFrame(video.word_list)
    # We do not need two end_time_s_x and end_time_s_y columns :)
    df2 = pd.DataFrame(video.amplitude_list).drop(columns=['end_time_s'])
    join_condition = ['start_time_s', 'url']
    df3 = dfHelper.customLeftJoin(df1, df2, join_condition)
    df4 = pd.DataFrame(video.pitch_list).drop(columns=['end_time_s'])  
    df5 = pd.merge(df3, df4, how='left', on=join_condition)
    #df5.to_csv("data_export.csv", header=True) # Export video breakdown to CSV
    #Export video breakdown to SQL
    df5.to_sql("test_table", con=engine, if_exists='append')
    df6 = pd.DataFrame(video.mfcc_list)
    #df6.to_csv("data_export_2.csv", header=True) # Export video breakdown to CSV
    df6.to_sql("mfcc_table", con=engine, if_exists='append')
    if TESTING:
        print(df1)
        print(df2)
        print(df4)
        print(df6)


##### Prompt for Highlight Video and Tagging #####
def prompt():
    answer = input("Option 1. single | Option 2. csv | Option 3. test \n")

    #If user wants to upload only a single video
    if answer == 'single' or answer == '1':
        url = input("Provide YT Link: ")
        tag = input("Provide highlight tag (True/False): ")
        print("Link: ", url)
        print("Tag: ", tag)

        #Check if video already exists
        url_exists = urlExists(url, engine)
        if url_exists == True:
            print("This video is already in the database! Did not export.")
        else:
            analyzeVideoSound(url, tag)

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

            #Check if video already exists
            url_exists = urlExists(url, engine)
            if url_exists == True:
                print("This video is already in the database! Did not export.")
            else:
                analyzeVideoSound(url, tag)

            i += 1
            print("\n --------------------------------")

    elif answer == 'test' or answer == '3':
        #Check if video already exists
        url_exists = urlExists(trump_video, engine)
        if url_exists == True:
            print("This video is already in the database! Did not export.")
        else:
            analyzeVideoSound(trump_video, True)


sqlConnectionSetup(engine)
prompt()