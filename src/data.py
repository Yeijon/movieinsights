"""
* 用来连接数据库的类
"""

import sqlite3
import sys
import logger

class database():
  # & 当实例化一个类即连接上数据库
  def __init__(self, databasename) -> None:
    self.databasename = databasename
    self.con = sqlite3.connect(databasename)
    
  def insert(self, datalist):
    log = logger.init_console_logger()
    cur = self.con.cursor()
    # 加入 name, director, autor, time, country, category, rate, disctription
    try:
      cur.execute("INSERT INTO movie(name, director, autor, year, country, category, rating, discription, movie_url) VALUES(?,?,?,?,?,?,?,?,?)", datalist)
      self.con.commit()
    except sqlite3.OperationalError as e:
      log.error(f"ERROR! Insertion failed: {e}")
      sys.exit()
    except ValueError as e:
      log.error(f"ERROR! Insertion failed: {e}")
      sys.exit()
    
  def select(self, name) -> tuple:
    log = logger.init_console_logger()
    cur = self.con.cursor()
    try:
      cur.execute("SELECT * FROM movie WHERE name=?", (name,))
      result = cur.fetchone() # & fetchone() 返回一个 tuple
      return result
    except ValueError as e:
      log.error(f"ERROR! Selection failed")
      log.exception(e)
      return None

  def clean_cache(self): 
    log = logger.init_console_logger()
    cur = self.con.cursor()
    try:
      cur.execute("DELETE FROM movie")
      self.con.commit()
    except sqlite3.OperationalError as e:
      log.error(f"ERROR! Clean cache failed: {e}")
      sys.exit()
    except ValueError as e:
      log.error(f"ERROR! Clean cache failed: {e}")
      sys.exit()

  def close(self):
    self.con.close()



  