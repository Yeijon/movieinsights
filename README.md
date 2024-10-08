# MovieInsights

> 见word文档有使用说明书

待进一步学习的点：
- python setup.cfg/poetry等工具流的的使用
- 进一步深入了解python的高级用法

## Develop Process

TODO: 

爬取top250作品，写入数据库并数据分析
- [x] 编写爬虫
  - [x] 封装成类
  - [x] config文件 解耦
- [x] 链接数据库的编写
- [x] gui，用tkinter
- [x] 数据分析和绘图
  - [x] 需要对电影题材/国家数据做二次处理
  - [x] 时间为轴，看电影题材的密集度变化 figure
  - [x] 不同国别时间的评分的变化 figure

![figure1](https://yeijon-note.oss-cn-beijing.aliyuncs.com/img/image-20240527130001846.png)
![figure2](https://yeijon-note.oss-cn-beijing.aliyuncs.com/img/image-20240527130020233.png)


通过命令行选取短评进行爬取，让AI统计分析大众情绪变化，然后输出词云图。

- [x] 添加简易的日志，便于测试 
- [x] 短评写入数据库中 
- [x] 编写爬虫逻辑，爬取一条写入对应的jsonl文件中 
- [x] 编写batch任务，得到导出数据 
- [x] 从导出数据中，编写词云图逻辑 
- [x] 编写命令行接口 
- [x] 将电影加入心愿单txt中


- [ ] ? 调用zhipu 大模型
  - [x] 构建 jsonl 文件：将数据库数据调入进去
  - [x] 编写batch任务
  - [ ] 导出数据，反馈给你的电影名单，整合起来 rich库/ 生成图片反馈到gui上

- [x] 命令行接口的设计

```shell
# 查询数据库中是否有该电影, 若存在，使用--requestAI 选项将自动使用AI进行标注并生成词云图
python main.py --requestAI search "your movie"
# 返回：
"YES! Here is some information about movie: xxx"
# 调用rich库编写markdown形式的
- Movie:
- Description:
- Rating:
- Country:
- Year:
# --requestAI
显示是否完成

# 执行爬虫得到结果，使用--analyze 将会把爬取得到的结果进行数据分析
python main.py --analyze scrape

```

TEST:
- [x] 数据连接测试：爬虫后，连接数据库
  - [x] 成功爬虫，打印出来测试成功
  - [x] 连接数据库并存入数据库中
- [x] 测试爬取数据并写入对应的jsonl文件中
- [x] 调用zhipu API是否顺利？ 历经诸多磨难，终于成功QAQ
- [x] 词云图的测试

参考资料：

[智谱AI开放平台](https://open.bigmodel.cn/dev/howuse/batchapi)

[sqlite3 --- DB-API 2.0 interface for SQLite databases — Python 3.12.3 文档](https://docs.python.org/zh-cn/3/library/sqlite3.html#sqlite3-tutorial)

[Python 项目工程化开发指南](https://pyloong.github.io/pythonic-project-guidelines/)

[Plotly Python Graphing Library](https://plotly.com/python/)
