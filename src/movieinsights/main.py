import json

from scraper import *
from gui import init_gui


def load_config():
  with open('config.json', 'r') as f:
    config = json.load(f)
    return config


def main():

  # TODO: 调用gui / 加载配置文件 / 执行爬虫 / 将数据导入数据库 / 绘图
  # 调用gui
  pages = int(init_gui())
  # 加载配置文件，主要是配置 爬虫的 请求头信息
  config = load_config()
  # 执行爬虫
  myscraper = Douban_MovieScraper(header=config['header'], start_page=0, end_page=pages)

  return None

if __name__ == '__main__':
  main()