import sqlite3

class database():
  def __init__(self, databasename) -> None:
    self.databasename = databasename
    self.con = sqlite3.connect(databasename)
    
  def insert(self, datalist):
    cur = self.con.cursor()
    # 加入 name, director, autor, time, country, category, rate, disctribtion
    cur.execute("INSERT INTO movie VALUES(?,?,?,?,?,?,?,?)", datalist)
    self.con.commit()
    
  def close(self):
    self.con.close()



  