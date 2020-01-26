import pymysql
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Numeric

#### SQL CONNECTION INFO ####
# Currently working on localhost
# MAKE SURE YOU HAVE A DATABASE CALLED 'climactic_test'

engine = create_engine('mysql+pymysql://root@localhost/climactic_test') # Make sure you use the correct username "root" and password

#SQL Connection Setup - Checks if table exists and if URL to be input already exists
def sqlConnectionSetup():
    global engine
    table_exists = False #Variable to check if table exists
    # Create a metadata instance
    meta = MetaData(engine)
    #meta.reflect(bind=engine)

    # Check if table already exists
    for _t in meta.tables:
        if _t == 'test_table': return

    # If table doesn't exist, create it
    if table_exists == False:
        # Declare a table
        table = Table('test_table',meta,
                    Column('id',Integer, primary_key=True, autoincrement=True),
                    Column('index',Integer),
                    Column('end_time_s',Integer),
                    Column('polarity',Float),
                    Column('start_time_s',Integer),
                    Column('subjectivity',Float),
                    Column('url',String(length=500)),
                    Column('word',String(length=500)),
                    Column('amplitude',Float),
                    Column('amplitude_peak',Integer),
                    Column('frequency', Float),
                )
        # Create all tables
        meta.create_all()

#Function checks if url exists in table already
def urlExists(url, isTest):
    if isTest == True: return False

    global engine
    # Check if URL already exists
    result = engine.execute('SELECT * FROM `test_table` WHERE `url`="' + url + '"')
    print("Number of rows in database for this video", result.rowcount)

    # If URL does exist return True
    return result.rowcount > 0