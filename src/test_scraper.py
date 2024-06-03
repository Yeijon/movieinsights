"""
* 目前还不太会pytest, 就是用最基本的unittest框架测试
"""

import unittest
from bs4 import BeautifulSoup as bs

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
        # TEST: 盗梦空间 PASS
        movie_scraper = scraper.Special_MovieScraper(movie_name="盗梦空间", header=self.header)
        # & 直接使用 fetch_data() 得到的列表在传导时存在读取问题
        test_url = "https://movie.douban.com/subject/3541415/comments?start=0&limit=20&status=P&sort=new_score"
        test_html = movie_scraper.request_web(test_url)
        self.assertNotEqual(test_html, "Errors")
        # self.assertRaises(requests.RequestException, movie_scraper.request_web(test_url[1]))
    
    def test_dissect_html(self):
        # TEST: 盗梦空间 PASS
        movie_scraper = scraper.Special_MovieScraper(movie_name="盗梦空间", header=self.header)
        test_url = "https://movie.douban.com/subject/3541415/comments?start=0&limit=20&status=P&sort=new_score"
        test_html = movie_scraper.request_web(test_url)
        test_soup = bs(test_html, 'lxml')
        result = movie_scraper.dissect_html(test_soup)
        # print(result)
        self.assertNotEqual(result, None)

    def test_parse_comment(self):
        # TEST: 盗梦空间 PASS
        movie_scraper = scraper.Special_MovieScraper(movie_name="盗梦空间", header=self.header)
        test_url = "https://movie.douban.com/subject/3541415/comments?start=0&limit=20&status=P&sort=new_score"
        test_html = movie_scraper.request_web(test_url)
        test_soup = bs(test_html, 'lxml')
        result = movie_scraper.dissect_html(test_soup)
        print(result)

    def test_data2jsonl(self):
        # TEST: "非常好看，特别是结尾，很有意思"
        test_str = "非常好看，特别是结尾，很有意思"
        data = scraper.data2jsonl(test_str)
        self.assertNotEqual(data, None)
        test_str2 = "情节相当悬疑，叙事很流畅，导演功力深厚，真不愧是诺兰，简直就是完美之作"
        data2 = scraper.data2jsonl(test_str2)
        self.assertEqual(data2, "Great!")
        


if __name__ == '__main__':
    unittest.main()

