"""
* 核心文件，定义了Douban_MovieScraper类由于爬取文件
"""

import re
import requests
from bs4 import BeautifulSoup as bs
import os

from data import database # 导入data.py中的类，这个文件名字取得不是很好，感觉容易误会成库

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

    def parse_item(self, item) -> list :
        try:
            # 图片
            item_pic = item.find('img')['src']

            # movie name
            item_names = item.find_all("span", class_='title')
            item_names_list = [i.text for i in item_names]
            item_names_zh = item_names_list[0] # & item_names_zh: str

            # director/autor/country/time 
            item_texts_temp = item.find('p', class_='').text
            item_text = self.dissect_text(item_texts_temp) # & item_text: list
            
            # rate
            item_rate = item.find(class_='rating_num').string # & item_rate: str

            # quote
            # & item_quote: str
            if item.find(class_='inq') is not None:
                item_quote = item.find(class_='inq').string
            else:
                item_quote = 'NOT AVAILABLE!'

            # TODO: 这个返回值 需要格式化一下 --> list FINISH
            # * 依照数据库的顺序： name/director/autor/time/contry/category/rate/discription
            item_list = item_text
            item_list.insert(0, item_names_zh)
            item_list.append(item_rate)
            item_list.append(item_quote)

            return item_list

        except AttributeError as e:
            print(f"Error parsing item: {e}")
            return None

    def dissect_text(self, text: str) -> list:
        # 返回的 剧情/国家/导演等黏在一起，通过此函数拆开
        item_text = []
        text = re.sub('.{2}:', "", text)
        s1 = text.split('\n')
        s2 = [s.split('\xa0') for s in s1]
        #print(f"\n\nTEST: s2: {s2}\n\n")
        # FIX: 会多出一个空格 FINISH
        for s in s2:
            s3 = [t.strip() for t in s if t.strip() != ''  and t != '/']
            item_text.extend(s3)

        #print(f"\n\nTEST: item_text: {item_text}\n\n")
        return item_text

    def dissect_html(self, soup):
        items = soup.find(class_='grid_view').find_all("li")
        
        # TODO: 待修整为数据流(sequence)导入数据库中 : 通过函数
        # & 实现测试，可以成功执行 
        for item in items:
            result = self.parse_item(item)
            # todo: 载入一个空文本中？
            if result:
               print(" | ".join(result))
            # TEST
            # BUG: 还是主键的问题，主键没有实现递增 FINISH
            storeData(result)
            

    def request_web(self, url):
        try:
            response = requests.get(url=url, headers=self.headers)
            if response.status_code == 200:
                return response.text
        except requests.RequestException:
            return "Errors"

    def run_scraper(self):
        urls = self.generate_url()

        # 爬取多页数据
        for url in urls:
          html_content = self.request_web(url=url)
          if html_content != "Errors":
            soup = bs(html_content, 'lxml')
            self.dissect_html(soup)

# TODO: 完成数据库连接
def storeData(result:list) -> None :
    # ! 已经自建了数据库，也许后面会考虑添加创建数据库 在 xxx/share 中
    # & 确定数据库文件的位置
    script_dir = os.path.dirname(__file__)
    db_path = os.path.join(script_dir, '../../share/Demo.sqlite')
    
    mydatabase = database(db_path) 
    mydatabase.insert(datalist=result)
    mydatabase.close()
    return None