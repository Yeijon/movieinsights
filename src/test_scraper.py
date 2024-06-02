"""
* 目前还不太会pytest, 就是用最基本的unittest框架测试
"""

import unittest
import requests

# BUG: 模块导入有问题

import os
import sys

#sys.path.append("E:\\prj\\MovieInsights\\movieinsights\\src")
#print(sys.path)

import scraper
from utils import load_config

class TestSpecialMovieScraper(unittest.TestCase):

    def setUp(self):
        self.config = load_config()
        self.header = self.config['header']

    def test_fatch_data(self):
        # TEST: 盗梦空间 PASS
        movie_scraper = scraper.Special_MovieScraper(movie_name="盗梦空间", header=self.header)
        test_url = movie_scraper.fatch_data()
        self.assertEqual(test_url, "https://movie.douban.com/subject/3541415/")
    
    def test_generate_url(self):
        # TEST: 盗梦空间 设定 n=2 PASS
        movie_scraper = scraper.Special_MovieScraper(movie_name="盗梦空间", header=self.header)
        test_url = movie_scraper.generate_url()
        print(f"TEST: test_urls: {test_url}")

    def test_request_web(self):
        # TEST: 盗梦空间
        movie_scraper = scraper.Special_MovieScraper(movie_name="盗梦空间", header=self.header)
        test_url = movie_scraper.fatch_data()
        test_html = movie_scraper.request_web((test_url[0]))
        self.assertNotEqual(test_html, "Errors")
        # self.assertRaises(requests.RequestException, movie_scraper.request_web(test_url[1]))
        


if __name__ == '__main__':
    unittest.main()

