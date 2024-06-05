"""
* This file is used to test the draw_wordcloud.py file
"""

import unittest

from utils import draw_wordcloud

class TestDrawWordCloud(unittest.TestCase):
    def test_draw_wordcloud(self):
        draw_wordcloud("盗梦空间")