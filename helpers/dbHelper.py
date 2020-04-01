import secrets
from sqlalchemy import create_engine
import pandas as pd


db_conn_str = "mysql+pymysql://{:}:{:}@{:}/{:}".format(secrets.user, secrets.password, secrets.host, secrets.db)


def insertRows(query):
  # Create connection
  engine = create_engine(db_conn_str)
  conn = engine.connect()
  # Begin transaction
  trans = conn.begin()
  conn.execute(query)
  trans.commit()
  # Close connection
  conn.close()


def getRowsAsDf(query):
  engine = create_engine(db_conn_str)
  df = pd.read_sql(query, con=engine)
  engine.dispose()
  return df


def urlExists(vidUrl):
  engine = create_engine(db_conn_str)
  query = "SELECT * from clips where url = '{:}'".format(vidUrl)
  df = pd.read_sql(query, con=engine)
  engine.dispose()
  return len(df) > 0


# input: column name as string, dataframe with updated column
def updateColumn(df, colName):
  engine = create_engine(db_conn_str)
  df.to_sql('temp_table', engine, if_exists='replace')
  sql = """
          UPDATE clips, temp_table
          SET clips.{:} = temp_table.{:}
          WHERE clips.url = temp_table.url 
            AND clips.start = temp_table.start;
  """.format(colName, colName)

  with engine.begin() as conn:     # TRANSACTION
      conn.execute(sql)

  engine.dispose()
