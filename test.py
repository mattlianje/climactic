import unittest
from run import run
import os


class MyTestCase(unittest.TestCase):

    def setUp(self):
        # Set environment variables
        os.environ['dev/prod'] = 'dev'
        # Trump video url
        video_url = 'https://www.youtube.com/watch?v=JZRXESV3R74'
        self.test_df = run(video_url)

    def test_pipeline_e2e(self):
        # Pipeline output should not be empty
        self.assertFalse(self.test_df.empty, 'Checking that df is not empty')

if __name__ == '__main__':
    unittest.main()
