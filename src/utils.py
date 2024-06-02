"""
* 这个文件存放一些常用的工具函数
"""

import os
import json


def load_config():
  with open('config.json', 'r') as f:
    config = json.load(f)
    return config


def get_DB_PATH() -> str:
    script_dir = os.path.dirname(__file__)
    DB_PATH = os.path.join(script_dir, '../share/Demo.sqlite')
    return DB_PATH
