"""
* 核心文件，定义了Douban_MovieScraper类由于爬取文件
"""

import re
import requests
from bs4 import BeautifulSoup as bs

class Douban_MovieScraper:
    def __init__(self, header,  base_url, start_page, end_page, step=25):
        self.base_url = base_url
        self.start_page = start_page
        self.end_page = end_page
        self.step = step
        self.headers = header

    def generate_url(self):
        return [self.base_url + f"?start={page * self.step}&filter=" \
                for page in range(self.start_page, self.end_page)]

    def parse_item(self, item):
        try:
            # 图片
            item_pic = item.find('img')['src']

            # movie name
            item_names = item.find_all("span", class_='title')
            item_names_list = [i.text for i in item_names]
            item_names_zh = item_names_list[0]

            # director/autor/country/time 
            item_texts_temp = item.find('p', class_='').text
            item_text = self.dissect_text(item_texts_temp)
            
            # rate
            item_rate = item.find(class_='rating_num').string

            # quote
            if item.find(class_='inq') is not None:
                item_quote = item.find(class_='inq').string
            else:
                item_quote = 'NOT AVAILABLE!'
            return item_names_zh, item_text, item_text, item_rate, item_quote
        except AttributeError as e:
            print(f"Error parsing item: {e}")
            return None

    def dissect_text(self, text: str) -> list:
        item_text = []
        text = re.sub('.{2}:', "", text)
        s1 = text.split('\n')
        s2 = [s.split('\xa0') for s in s1]

        for s in s2:
            s3 = [t.strip() for t in s if t != '' and t != '/']
            item_text.extend(s3)

        return item_text

    def dissect_html(self, soup):
        items = soup.find(class_='grid_view').find_all("li")
        
        # TODO:
        for item in items:
            result = self.parse_item(item)
            if result:
                print(" | ".join(result))

    def request_web(self, url):
        try:
            response = requests.get(url=url, headers=self.headers)
            if response.status_code == 200:
                return response.text
        except requests.RequestException:
            return "Errors"

    def run_scraper(self):
        urls = self.generate_url()

        for url in urls:
          html_content = self.request_web(self.base_url)
          if html_content != "Errors":
            soup = bs(html_content, 'lxml')
            self.dissect_html(soup)
