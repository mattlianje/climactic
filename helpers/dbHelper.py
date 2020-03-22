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
