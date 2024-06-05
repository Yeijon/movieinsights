"""
* 测试zhipu ai的相关代码
"""

import unittest
from utils import load_config
from zhipu_batch import batch_task, batch_download

# BUG： 传参有问题 --> 
# When using unittest in Python to test functions \
# that involve floating-point numbers, \
# you may notice extra 'E's in the output due to scientific notation.
class TestZhipuai(unittest.TestCase):
    def test_batch_task(self):
        APIKEY = "33ca1f7de4516dddaf96e207802961fa.bNNpgRQ6Gapb5UCl"
        
        batch = batch_task(APIKEY)
        
        with open('store_batch_id.txt', 'a') as f:
            f.write(batch.id)
            f.close()
        
        self.assertEqual(batch.status, "in_progress")
    
    def test_batch_download(self):
        batch = batch_task(self.APIKEY)
        result = batch_download(self.APIKEY, batch.output_file_id)
        self.assertIsNone(result)
