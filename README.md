# MovieInsights

## 1. Overview

A python project for final homework.

## 2. Usage

### 2.1 init project

```bash
poetry install -v
```

### 2.2 usage

TODO

## 3. Develop

You may need to read the [develop document](./docs/development.md) to use SRC Layout in your IDE.

## 4. Develop Process

TODO: 
- [x] 编写爬虫
  - [x] 封装成类
  - [x] config文件 解耦
- [x] 链接数据库的编写
- [x] gui，用tkinter
- [ ] 数据分析和绘图
  - [ ] 二维图：
    - [ ] 需要对电影题材/国家数据做处理
    - [ ] 时间为轴，看电影题材的密集度
    - [ ] 时间的评分的变化
    - [ ] 不同国家电影Top前xx的比重和综合评分

- [ ] 添加简易的日志，便于测试
- [ ] ? 调用zhipu 大模型
  - [ ] 构建 jsonl 文件：将数据库数据调入进去
  - [ ] 编写batch任务
  - [ ] 导出数据，反馈给你的电影名单，整合起来 rich库/ 生成图片反馈到gui上

TEST:
- [x] 数据连接测试：爬虫后，连接数据库
  - [x] 成功爬虫，打印出来测试成功
  - [x] 连接数据库并存入数据库中

参考资料：
[智谱AI开放平台](https://open.bigmodel.cn/dev/howuse/batchapi)
[sqlite3 --- DB-API 2.0 interface for SQLite databases — Python 3.12.3 文档](https://docs.python.org/zh-cn/3/library/sqlite3.html#sqlite3-tutorial)
[Python 项目工程化开发指南](https://pyloong.github.io/pythonic-project-guidelines/)