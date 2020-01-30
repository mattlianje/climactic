# lib of methods to aggregate, and transform audio dataframes
import pandas as pd
from scipy.signal import find_peaks

# customLeftJoin
#
# input ...
# dfLeft <- pandas df
# dfRight <- pandas df
# leftCols <- columns the join is done on. (IMPORTANT right now it assumes the same columns are named the same in both df's)
#
# output ...
# returns pandas df with numrows = numrows dfLeft

def customLeftJoin(dfLeft, dfRight, joinCondition):

    joinedDf = pd.merge(dfLeft, dfRight, how='left', left_on=joinCondition, right_on=joinCondition)
    # indices <- list of time stamps of amplitude peaks
    indices = find_peaks(dfRight['amplitude'])[0]
    for index, row in joinedDf.iterrows():
        if row['start_time_s'] not in indices:
            joinedDf.at[index, 'amplitude_peak'] = False
        else:
            joinedDf.at[index, 'amplitude_peak'] = True

    return joinedDf

def checkJoin(dfLeft, dfRight, joinDescription):
    if (dfLeft.shape[0] == dfRight.shape[0]):
        print('Join on "', joinDescription ,'" successful!')
    else:
        print('Join on "', joinDescription ,'" failed ...')