from sqlalchemy.orm import sessionmaker
import lib.etl.sqlConnection as sqlConnection
from sklearn.cluster import KMeans

engine = sqlConnection.getEngine(False)
Session = sessionmaker(bind = engine)
session = Session()

def customKMeans(table_name, k_value, column_list):
    kMeansDf = sqlConnection.getTableAsDf(table_name)
    kMeansDf_formatted = kMeansDf[column_list]

    kmeans = KMeans(n_clusters=k_value, random_state=0).fit(kMeansDf_formatted)
    # result = session.query(table_name).filter(table_name.url == url)

    print(kmeans.cluster_centers_)
    # Select only columns that have numeric values that we will be using

