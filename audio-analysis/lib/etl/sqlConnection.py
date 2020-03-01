import pymysql
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Numeric
from secrets import db_username, db_password
import sqlalchemy as db
import pandas as pd

#### SQL CONNECTION INFO ####
# MAKE SURE YOU HAVE A DATABASE CALLED 'climactic_test'


def getEngine(isTest):
    if isTest:
        try:
            engine = create_engine('mysql+pymysql://root:root@localhost/climactic_test')
            engine.connect()
            print("\nYou are connected to ", engine, "\n")
        except Exception:
            engine = create_engine('mysql+pymysql://root:root@localhost:8889/climactic_test')
            engine.connect()
            print("\nYou are connected to ", engine, "\n")
        except:
            print("\n ERROR: Issues connecting to your localhost \n")
            
    else:
        try:
            engine = create_engine('mysql+pymysql://' + db_username + ':' + db_password + '@climactic-test.cmikkru8vljn.us-east-1.rds.amazonaws.com:3306/climactic_test')
            engine.connect()
            print("\nYou are connected to ", engine, "\n")
        except:
            print("\n ERROR: Issues connecting to the AWS database \n")
    
    return engine

#SQL Connection Setup - Checks if table exists and if URL to be input already exists
def sqlConnectionSetup(engine):
    table_exists = False # Variable to check if table exists
    meta = MetaData(engine) # Create a metadata instance
    tables = ['test_table', 'mfcc_table']
    
    for _t in tables:
        if tableExists(_t, meta) == False:
            print('Table "', _t,'" does not exist. Creating..')
            createTable(_t, meta, engine)
    
    meta.create_all() # Create all tables

#Function checks if url exists in table already
def urlExists(url, engine):
    # Check if URL already exists
    result = engine.execute('SELECT * FROM `test_table` WHERE `url`="' + url + '"')
    print("Number of rows in database for this video", result.rowcount)

    # If URL does exist return True
    return result.rowcount > 0

def tableExists(table_name, meta):
    # Check if table already exists
    for _t in meta.tables:
        if _t == table_name: return True
    return False

def createTable(table_name, meta, engine):
    #Creates the Test Table
    if table_name == 'test_table':
        test_table = Table(table_name,meta,
                    Column('id',Integer, primary_key=True, autoincrement=True),
                    Column('index',Integer),
                    Column('end_time_s',Integer),
                    Column('polarity',Float),
                    Column('start_time_s',Integer),
                    Column('subjectivity',Float),
                    Column('url',String(length=500)),
                    Column('video_title', String(length=500)),
                    Column('word',String(length=500)),
                    Column('amplitude',Float),
                    Column('amplitude_peak',Integer),
                    Column('pitch',Float),
                    Column('p_confidence',Float),
                )
    elif table_name == 'mfcc_test_table':
        mfcc_table = Table(table_name,meta,
                    Column('mfcc_id',Integer, primary_key=True, autoincrement=True),
                    Column('index',Integer),
                    Column('end_time_s',Integer),
                    Column('start_time_s',Integer),
                    Column('url',String(length=500)),
                )
        for i in range (1,60):
            engine.execute('ALTER TABLE `'+ table_name +'` ADD mfcc_'+ '{0:0=2d}'.format(i) +' float;')
    else:
        print('ERROR: There is not setup for table "', table_name, '". Please create its setup.')


def getTableAsDf(table_name):
    engine = getEngine(False)
    metadata = db.MetaData()
    table_obj = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
    query = db.select([table_obj])
    result_proxy = engine.execute(query)
    result_set = result_proxy.fetchall()
    result_df = pd.DataFrame(result_set)
    result_df.columns = result_set[0].keys()
    return result_df
