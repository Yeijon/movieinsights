""" 编写爬虫代码 """
import requests
from bs4 import BeautifulSoup as bs
import re

def dissect_texts(texts:list) -> dict :
  texts = re.sub(r'.{2}:|\xa0'," ", texts) # 去除掉从html中残留的空格字符等
  del texts[0]
  del texts[-1] # ? 有没有更优雅的方式？
  
  # 由于’/‘黏在一起，需要分开拆
  creators = [c.strip() for c in texts[0].split("   ")]
  classification = [c.strip() for c in texts[-1].split("/")]

  dict2 = dict(zip(["导演","主演"], creators))
  dict1 = dict(zip(["时间", "国家", "类别"], classification))
  return {**dict1,**dict2}

def dissect_html(soup):
  items = soup.find(class_='grid_view').find_all("li")
  
  for item in items:
    # 图片链接
    item_pic = item.find('img')['src']
    # 中文名 + 英文名
    item_names = item.find(class_='title')
    ## 分割内容
    item_names_list = [i.text for i in item_names]
    item_names_zh = item_names_list[0]
    item_names_en = re.sub(r'\xa0/\xa0','',item_names_list[1])

    # 情况
    item_texts_temp = soup.find('p', class_='').text
    
    item_texts_dicts = dissect_texts(item_texts_temp)

    # 评分
    item_rate = item.find(class_='rating_num').string
    # quote
    if item.find(class_='inq') is not None:
      item_quote = item.find(class_='inq').string
    else:
      item_quote = 'NOT AVALABLE!'

    
  return None

# TODO: 获取剧情介绍？

def request_web(url):
  headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
               }
  try:
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
      return response.text
  except requests.RequestException:
    return None

def main():
  # url
  url = "https://movie.douban.com/top250?start=50&filter="
  html = request_web(url)
  soup = bs(html,'lxml')
  dissect_html(soup)


if __name__ == '__main__':
  main()