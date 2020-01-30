import unittest
import lib.etl.dfHelper as dfHelper
import pandas as pd

class AudioUnitTests(unittest.TestCase):

    def test_custom_left_join(self):
        df1 = pd.DataFrame({'word': ['dj', 'trump'], 'start_time_s': [1580358006, 1580358007]})
        df2 = pd.DataFrame({'amplitude': [300, 350, -100], 'start_time_s': [1580358006, 1580358007, 1580358008]})
        join_condition = ['start_time_s']
        df3 = dfHelper.customLeftJoin(df1, df2, join_condition)
        # Assert on number of rows of left df == number of rows joined df.
        self.assertEqual(df1.shape[0], df3.shape[0])

if __name__ == '__main__':
    unittest.main()