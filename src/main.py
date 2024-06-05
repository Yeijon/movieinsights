from rich.console import Console
import click
from typing import Optional

from scraper import *
from gui import init_gui
import graph
from data import *
from utils import load_config, get_DB_PATH, get_movie_info, draw_wordcloud
from zhipu_batch import batch_task, batch_download

# *----------------------------------- 常量 -----------------------------------* #
# 加载配置文件，主要是配置 爬虫的 请求头信息
config = load_config()
# 从配置文件中获取 zhipu 的 API KEY
APIKEY = config['zhipu_API_KEY']
BATCH_ID = None
ID_NUM = 0

# *--------------------------------- 文件入口 main --------------------------------* #
@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):

  if ctx.invoked_subcommand is None:
    return run(analyze=True)

# *-------------------------- 核心功能1：执行爬虫爬取豆瓣电影top250 -------------------------- #
@main.command(help="Execute a crawler to crawl the top 250 movies on Douban")
@click.option(
  '--analyze',
  type=bool,
  default=True,
  required=False,
  help="Whether to analyze the data and generate Graphs for analysis"
)
def run(analyze:bool):
  # 清除数据库中的缓存
  # BUG: UnboundLocalError: local variable 'database' referenced before assignment
  """ db = database("../../share/Demo.sqlite")
  db.clean_cache()
  db.close() """

  # * 调用gui / 加载配置文件 / 执行爬虫 / 将数据导入数据库 / 绘图
  # 调用gui
  pages = init_gui()
  print(f"\n\tLogging: pages = {pages}\n")

  # 执行爬虫
  myscraper = Douban_MovieScraper(header=config['header'], base_url="https://movie.douban.com/top250",start_page=0, end_page=pages)
  myscraper.run_scraper()
  
  if analyze:
    # 绘图
    db_path = get_DB_PATH()
    graph.process_movie_data(db_path)

  return None

# * 单独进行绘图的命令
@main.command(help="Generate Graphs for analysis")
def draw():
  db_path = get_DB_PATH()
  graph.process_movie_data(db_path)
  return None

# *------------------------- 核心功能2：查询电影，使用AI自动标注和生成词云图 ------------------------* #
@main.command(help="Query whether the movie exists in the database, if exists, return the information and generate a word cloud diagram.")
@click.option(
  '--requestAI',
  type=bool,
  default=False,
  required=False,
  help="AI will be automatically used to annotate and generate word cloud diagrams. (Model: GLM-4[Batch API -- zhipu.ai])"
)
@click.argument('movie_name', type=str, required=True, nargs=1)
#@click.pass_context
def search(movie_name:str, requestai: Optional[bool] = False):
  # TODO: 从数据库中查询是否存在该电影
  mydatabase = database(get_DB_PATH())
  result = mydatabase.select(name=movie_name)

  console = Console()

  # 存在则返回信息，并根据 requestAI 决定是否调用 AI
  if result:
    get_movie_info(result)

    if requestai:

      mymoviescraper = Special_MovieScraper(movie_name=movie_name, header=config['header'])
      mymoviescraper.run_scraper()
      # 调用zhipu的api
      # TEST
      batch = batch_task(APIKEY)
      # & batch_id要存一下，因为batch调用很慢
      BATCH_ID = batch.id

      if batch.status == "in_progress":
        console.print("请等待AI处理数据，生成词云图...\n")
        return None

      #batch_download(APIKEY, batch.output_file_id)
    else:
      # 创建该电影txt文件
      with open(f'../share/{movie_name}_comment.txt', 'w', encoding='utf-8') as f:
        f.write(f'{movie_name}的评论\n')
        f.close()
      mymoviescraper = Special_MovieScraper(movie_name=movie_name, header=config['header'])
      mymoviescraper.run_scraper()

      # TODO： 从test_comment.txt中提取，生成词云图 FINISH
      draw_wordcloud(movie_name)
      return 1
  else:
    console.print(f"\n\t[bold red]电影[/bold red]: {movie_name} 不存在数据库中\tQAQ\n")
    return -1

if __name__ == '__main__':
  main()