import lib.models.voronoiClassifier as voronoiClassifier
import lib.etl.sqlConnection as sqlConnection

voronoiClassifier.customKMeans('test_table', 8, ['amplitude', 'pitch'], [[2, 12], [0, 1]])
