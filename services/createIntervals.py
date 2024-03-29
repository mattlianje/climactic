from helpers import dbHelper


# returns interval start and end times
def getIntervals(duration, intervalLength, overlapLength):
  intervals = []
  startTime = 0
  endTime = startTime + intervalLength

  while endTime <= duration:
    intervals.append([startTime, endTime])
    startTime = endTime - overlapLength
    endTime = startTime + intervalLength

  if endTime > duration:
    intervals.append([startTime, duration])

  return intervals


# helper function to format vidUrl and interval
def formatValues(vidUrl, interval):
  return "('{:}', {:}, {:})".format(vidUrl, interval[0], interval[1])


# creates rows in db with interval start, end, and yt url
def insertIntervals(vidUrl, intervals):
  if not dbHelper.urlExists(vidUrl):
    rowValues = list(map(lambda x: formatValues(vidUrl, x), intervals))
    query = "INSERT INTO clips (url, start, end) VALUES {:}".format(",".join(rowValues))
    dbHelper.insertRows(query)
