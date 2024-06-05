"""
* 这个文件存放一些常用的工具函数
"""

import os
import json
from rich.console import Console
import jieba
import wordcloud

def load_config():
  with open('config.json', 'r') as f:
    config = json.load(f)
    return config

def get_DB_PATH() -> str:
    script_dir = os.path.dirname(__file__)
    DB_PATH = os.path.join(script_dir, '../share/Demo.sqlite')
    return DB_PATH

def get_movie_info(result:tuple) -> None:
  """
  * 从电影中返还数据到终端
  """
  console = Console()
  console.print(f"\n\t[bold red]电影信息[/bold red]\n")
  console.print(f"\t[orange]电影名称[/orange]: {result[1]}")
  console.print(f"\t导演: {result[2]}")
  console.print(f"\t[green]上映时间[/green]: {result[4]}")
  console.print(f"\t[blue]国家[/blue]: {result[5]}")
  console.print(f"\t[yellow]类型[/yellow]: {result[6]}")
  console.print(f"\t评分: {result[7]}")
  console.print(f"\t[italic]简介[/italic]: {result[8]}\n")

  return None

# TODO: 编写词云图逻辑
def draw_wordcloud(movie_name:str):
  """
  * 生成词云图
  """
  wc = wordcloud.WordCloud(
    font_path=r'C:\\Windows\\Fonts\\dengl.ttf',
    background_color='white',
    width=800,
    height=600,
    max_words=200,
    max_font_size=100,
    min_font_size=20
  )

  with open('test_comment.txt', 'r', encoding='utf-8') as f:
    comment = f.read()
    words = jieba.cut(comment, cut_all=True)
    wc.generate(' '.join(words))

    wc.to_file(f'{movie_name}_worldcloud.png')

  return None