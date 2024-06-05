"""
* 测试main.py中的函数 search()
"""

import unittest

from main import search

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.movie_name = "测试"
        self.requestai = False
    def test_search(self):
        result = search(self.movie_name, self.requestai)
        self.assertEqual(result, -1)


