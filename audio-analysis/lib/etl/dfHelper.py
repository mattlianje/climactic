# lib of methods to aggregate, and transform audio dataframes
import pandas as pd

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
    return joinedDf