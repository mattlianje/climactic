import mysql.connector
import secrets
from mysql.connector import errorcode

config = {
  'user': secrets.user,
  'password': secrets.password,
  'host': secrets.host,
  'database': secrets.db,
  'raise_on_warnings': True
}

def urlExists(url):
  cnx = mysql.connector.connect(**config)
  cursor = cnx.cursor()

  query = "SELECT url FROM labelled WHERE url = '{:}' ".format(url)
  cursor.execute(query)

  rowCount = 0
  for url in cursor:
    rowCount += 1

  cursor.close()
  cnx.close()

  return rowCount > 0

def getIntervals(url):
  cnx = mysql.connector.connect(**config)
  cursor = cnx.cursor()

  query = "SELECT start, end FROM labelled WHERE url = '{:}' ".format(url)
  cursor.execute(query)

  intervals = []
  for (start, end) in cursor:
    intervals.append((start, end))

  cursor.close()
  cnx.close()

  return intervals
