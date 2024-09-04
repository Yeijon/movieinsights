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

# TODO: 编写词云图逻辑 FINISH
def draw_wordcloud(movie_name:str):
  """
  * 生成词云图
  """
  wc = wordcloud.WordCloud(
    font_path=r'C:\\Windows\\Fonts\\dengl.ttf',
    background_color='white',
    width=800,
    height=600,
    max_words=300,
    max_font_size=100,
    min_font_size=20,
    stopwords=['电影', '一部', '一个', '这部', '这个', '那个', '那部', '这是', '那是', '这么', '那么', '这样', '那样', '这种', '那种', '这里', '那里', '这些', '那些', '这时', '那时', '这次', '那次', '这么', '那么', '这样', '那样','的', '很', '都', '有', '在', '太', '什么', '被', '对', '是', '从']
  )

  with open(f'../share/{movie_name}_comment.txt', 'r', encoding='utf-8') as f:
    comment = f.read()
    words = jieba.cut(comment, cut_all=True)
    wc.generate(' '.join(words))

    wc.to_file(f'../share/{movie_name}_worldcloud.png')

  return None


# TODO: 喜欢该电影就进入清单中吧！ 
def add_to_list(result:tuple) -> None:
  """
  * 将电影添加到清单中
  """
  with open('../share/movie_list.txt', 'a', encoding='utf-8') as f:
    f.write(f'电影名称：{result[1]}\n')
    f.write(f'导演：{result[2]}\n')
    f.write(f'上映时间：{result[4]}\n')
    f.write(f'国家：{result[5]}\n')
    f.write(f'类型：{result[6]}\n')
    f.write(f'评分：{result[7]}\n')
    f.write(f'简介：{result[8]}\n\n')
    f.close()
  return None