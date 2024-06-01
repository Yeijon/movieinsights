"""
* 核心文件，定义了Douban_MovieScraper类由于爬取文件
"""

import re
import requests
from bs4 import BeautifulSoup as bs
import os
import sys
import json

from data import database # 导入data.py中的类，这个文件名字取得不是很好，感觉容易误会成库
import logger

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
        """
        爬虫，匹配值
        """
        try:
            # 图片：未被使用到
            # item_pic = item.find('img')['src']
            # TODO:
            # * movie_url 该电影的链接
        # ? 有些纳闷这里，为什么使用 item.find('div.class', class_='pic').a['href'] 会找不到 ？？？
            item_movie_url = item.find('div', class_='pic').a['href']

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
            # * 依照数据库的顺序： name/director/autor/time/contry/category/rate/discription/movie_url
            item_list = item_text
            item_list.insert(0, item_names_zh)
            item_list.append(item_rate)
            item_list.append(item_quote)
            item_list.append(item_movie_url)

            return item_list

        except AttributeError as e:
            log = logger.init_console_logger()
            log.error(f"Error parsing item.")
            log.exception(e)
            return None

    def dissect_text(self, text: str) -> list:
        """
        返回的 剧情/国家/导演等黏在一起，通过此函数拆开
        """
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

# TODO: 完成数据库连接 FINISH
def storeData(result:list) -> None :
    # ! 已经自建了数据库，也许后面会考虑添加创建数据库 在 xxx/share 中
    # & 确定数据库文件的位置
    script_dir = os.path.dirname(__file__)
    db_path = os.path.join(script_dir, '../../share/Demo.sqlite')
    
    mydatabase = database(db_path) 
    mydatabase.insert(datalist=result)
    mydatabase.close()
    return None

# TODO: 编写爬虫电影短片的类
class Special_MovieScraper:
    def __init__(self, movie_name, header):
        # TODO: 从命令行传过来
        self.movie_name = movie_name
        self.headers = header

    # * 是否存在数据库中，从命令行传过来
    def fatch_data(self):
        
        script_dir = os.path.dirname(__file__)
        db_path = os.path.join(script_dir, '../../share/Demo.sqlite')

        mydatabase = database(db_path)
        result = mydatabase.select(name=self.movie_name)

        # TODO: 待后续结合命令行，输出到命令行
        return result[-1] # 返回  movie_url

    # * 从数据库中提取并爬取短评，然后绘制成词云图

    def generate_url(self):
        base_url = self.fatch_data()
        # 抓取前n页的评论，每条20条评论
        n = 25

        return [self.base_url + f"comments?start={page * 20}&limit=20&status=P&sort=new_score" \
                for page in range(0, n)]

    def request_web(self, url):
        try:
            response = requests.get(url=url, headers=self.headers)
            if response.status_code == 200:
                return response.text
        except requests.RequestException:
            return "Errors"
    
    def parse_comment(self, comment) -> str:
        try:
            comment_text = comment.find('span', class_='short').text
            return comment_text
        except Exception as e:
            log = logger.init_console_logger()
            log.error(f"Error parsing comment.")
            log.exception(e)
            return None

    def dissect_html(self, soup) -> None:
        comments = soup.find_all(class_='comment')
        for comment in comments:
            result = self.parse_comment(comment)
            # TODO: 编写 zhipu ai 的相关代码
            if result:
                data2jsonl(result)
        return None


    def run_scraper(self):
        urls = self.generate_url()

        for url in urls:
            html_content = self.request_web(url=url)
            if html_content != "Errors":
                soup = bs(html_content, 'lxml')
                self.dissect_html(soup)


# TEST 
def data2jsonl(comment_text: str) -> None:
    """
    将评论数据存储为jsonl格式
    json对象的格式：

    {
        "custom_id": "request-1",  #每个请求必须包含custom_id且是唯一的,长度必须为 6 -64 位.用来将结果和输入进行匹配.
        "method": "POST",
        "url": "/v4/chat/completions", 
        "body": {
            "model": "glm-4",     #每个batch文件只能包含对单个模型的请求,支持 glm-4、glm-3-turbo.
            "messages": [
                {"role": "system","content": "你是一个针对电影评论的意图分类器"},
                {"role": "user", "content": 
                '''
                # 任务：对以下用户的电影短评评论进行观影情绪分类和观影评价标注，只输出结果。
                # 观影情绪分类词建议：钦佩、崇拜、欣赏、娱乐、焦虑、敬畏、尴尬、厌倦、冷静、困惑、渴望、厌恶、痛苦、着迷、嫉妒、兴奋、恐惧、痛恨、有趣、快乐、怀旧、浪漫、悲伤、满意、性欲、同情、满足、愉悦等
                # 观影评价标注选词建议：导演：执导得当、导演功力深厚、导演手法独特；演员：演技精湛、表演自然、角色诠释到位；镜头：镜头运用巧妙、镜头切换流畅、镜头构图新颖；摄影：摄影角度独特、画面质感出色、摄影手法精湛；剧情：剧情紧凑、情节跌宕起伏、剧情发展合理；线索：线索设计巧妙、线索铺陈自然、线索逻辑清晰；环境：环境营造恰到好处、场景布置精心、环境氛围感强烈；色彩：色彩搭配和谐、色彩运用巧妙、色彩表现丰富；光线：光线处理恰到好处、光线效果炫目、光线照射角度合理；视听语言：视听语言独具匠心、声音效果震撼、音乐配合恰到好处；道具作用：道具运用恰到好处、道具设计别具匠心、道具作用明显；转场：转场处理流畅、转场设计巧妙、转场效果引人入胜；剪辑：剪辑节奏紧凑、剪辑处理精湛、剪辑效果出色 等等
                # 评论：review = "情节相当悬疑，叙事很流畅，导演功力深厚，真不愧是诺兰，简直就是完美之作。"
                # 输出格式：
                {
                    "情绪分类标签": "愉悦 赞赏", 
                    "观影评价标注": "紧扣剧情 叙事流畅 大导演" 
                    }
                '''
                }
            ],
        "temperature": 0.1
        }
    }
    """
    global idn
    idn += 1
    data = {
        "custon_id": f"request-{idn}",
        "method": "POST",
        "url": "/v4/chat/completions",
        "body": {
            "model": "glm-4",
            "messages": [
                {"role": "system", "content": "你是一个针对电影评论的意图分类器"},
                {"role": "user", "content": 
                """
                # 任务：对以下用户的电影短评评论进行观影情绪分类和观影评价标注，只输出结果。
                # 观影情绪分类词建议：钦佩、崇拜、欣赏、娱乐、焦虑、敬畏、尴尬、厌倦、冷静、困惑、渴望、厌恶、痛苦、着迷、嫉妒、兴奋、恐惧、痛恨、有趣、快乐、怀旧、浪漫、悲伤、满意、性欲、同情、满足、愉悦等
                # 观影评价标注选词建议：导演：执导得当、导演功力深厚、导演手法独特；演员：演技精湛、表演自然、角色诠释到位；镜头：镜头运用巧妙、镜头切换流畅、镜头构图新颖；摄影：摄影角度独特、画面质感出色、摄影手法精湛；剧情：剧情紧凑、情节跌宕起伏、剧情发展合理；线索：线索设计巧妙、线索铺陈自然、线索逻辑清晰；环境：环境营造恰到好处、场景布置精心、环境氛围感强烈；色彩：色彩搭配和谐、色彩运用巧妙、色彩表现丰富；光线：光线处理恰到好处、光线效果炫目、光线照射角度合理；视听语言：视听语言独具匠心、声音效果震撼、音乐配合恰到好处；道具作用：道具运用恰到好处、道具设计别具匠心、道具作用明显；转场：转场处理流畅、转场设计巧妙、转场效果引人入胜；剪辑：剪辑节奏紧凑、剪辑处理精湛、剪辑效果出色 等等
                # 例如：
                - 评论：review = "情节相当悬疑，叙事很流畅，导演功力深厚，真不愧是诺兰，简直就是完美之作。"
                - 输出格式：
                {
                    "情绪分类标签": "愉悦 赞赏", 
                    "观影评价标注": "紧扣剧情 叙事流畅 大导演" 
                }

                # 评论：review = f"{comment_text}"
                # 输出格式：
                {
                    "情绪分类标签": " ",
                    "观影评价标注": " "
                }
                """
                }
            ]
        },
    }
    log = logger.init_logger()
    try:
        with open('comment.jsonl', 'w', encoding='utf-8') as f:
            # 依照jsonl格式写入数据
            f.write(json.dump(data, f, ensure_ascii=False))
            f.close()
        log.info(f"Data has been written to comment.jsonl.")
    except Exception as e:
        log = logger.init_console_logger()
        log.error(f"Error writing data to comment.jsonl.")
        log.exception(e)
    return None
    