import lib.models.voronoiClassifier as voronoiClassifier
import lib.etl.sqlConnection as sqlConnection

voronoiClassifier.customKMeans('test_table', 2, ['amplitude', 'pitch'])
