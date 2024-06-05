"""
* 测试main.py中的函数 search()
"""

import unittest

from main import search

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.movie_name = "盗梦空间"
        self.requestai = True
    def test_search(self):
        result = search(self.movie_name, self.requestai)
        self.assertIsNone(result)


