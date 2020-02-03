from sqlalchemy.orm import sessionmaker
import lib.etl.sqlConnection as sqlConnection
from sklearn.cluster import KMeans
from scipy.spatial import Voronoi, voronoi_plot_2d, cKDTree
import matplotlib.pyplot as plt
import numpy as np
import math


engine = sqlConnection.getEngine(False)
Session = sessionmaker(bind = engine)
session = Session()

def customKMeans(table_name, k_value, column_list, prediction_observation):
    kMeansDf = sqlConnection.getTableAsDf(table_name)
    kMeansDf_formatted = kMeansDf[column_list]

    kmeans = KMeans(n_clusters=k_value, random_state=0).fit(kMeansDf_formatted)

    # Take all the cluster centers and find the 'highlight' cluster using a heuristic
    # Assumption: The further the centroid of a cluster is from the origin o(i, j ... n) the more ...
    # highlight likely the moment is.

    max_d_from_origin = 0
    # highlight centroid is the list of coordinates of the centre of the voronoi cell in our ...
    # k-means hyperplane that
    highlight_centroid = kmeans.cluster_centers_[0]

    for center in kmeans.cluster_centers_:
        total_dst = 0
        for i in range(len(center)):
            current_dim = center[i] ** 2
            if i == 0:
                total_dst = current_dim
            else:
                total_dst = total_dst + current_dim
        eucl_d_from_origin = math.sqrt(total_dst)

        if eucl_d_from_origin > max_d_from_origin:
            max_d_from_origin = eucl_d_from_origin
            highlight_centroid = center

    # Graphs the tessellation
    tessellation = Voronoi(kmeans.cluster_centers_)
    voronoi_plot_2d(tessellation)
    plt.show()

    # Voronoi binary trie with each node being an axis ...
    voronoi_tree = cKDTree(kmeans.cluster_centers_)
    # Regions of the tessellation to which our new observations belong to
    prediction_observation_regions = voronoi_tree.query(prediction_observation)
    print(prediction_observation_regions)


