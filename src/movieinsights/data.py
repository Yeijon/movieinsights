"""
* 用来连接数据库的类
"""

import sqlite3
import sys

class database():
  # & 当实例化一个类即连接上数据库
  def __init__(self, databasename) -> None:
    self.databasename = databasename
    self.con = sqlite3.connect(databasename)
    
  def insert(self, datalist):
    cur = self.con.cursor()
    # 加入 name, director, autor, time, country, category, rate, disctription
    try:
      cur.execute("INSERT INTO movie(name, director, autor, time, country, category, rate, discription) VALUES(?,?,?,?,?,?,?,?)", datalist)
      self.con.commit()
    except sqlite3.OperationalError as e:
      print("ERROR! Columns doesn't match.\n")
      print(e)
      sys.exit()
    
  def close(self):
    self.con.close()



  