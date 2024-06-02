import json

from scraper import *
from gui import init_gui
import graph
from data import *
from utils import load_config, get_DB_PATH

def main():

  # 清除数据库中的缓存
  # BUG: UnboundLocalError: local variable 'database' referenced before assignment
  """ db = database("../../share/Demo.sqlite")
  db.clean_cache()
  db.close() """

  # TODO: 调用gui / 加载配置文件 / 执行爬虫 / 将数据导入数据库 / 绘图
  # 调用gui
  pages = init_gui()
  print(f"\n\tLogging: pages = {pages}\n")
  # 加载配置文件，主要是配置 爬虫的 请求头信息
  config = load_config()
  # 执行爬虫
  myscraper = Douban_MovieScraper(header=config['header'], base_url="https://movie.douban.com/top250",start_page=0, end_page=pages)
  myscraper.run_scraper()
  
  # 绘图
  db_path = get_DB_PATH()
  graph.process_movie_data(db_path)

  return None

if __name__ == '__main__':
  main()