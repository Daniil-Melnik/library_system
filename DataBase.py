from flask import url_for


class DataBase:
  def __init__(self, db):
    self.__db = db
    self.__cur = db.cursor()
  
  def getBooks(self):
    sql = '''SELECT * FROM dmel_books'''
    try:
      self.__cur.execute(sql)
      res = self.__cur.fetchall()
      if res: return res
    except:
      print("Ошибка чтения из БД")
    return []
  
  def getBook(self, book_id):
    try:
      self.__cur.execute(f"SELECT * FROM dmel_books WHERE id = '{book_id}' LIMIT 1")
      res = self.__cur.fetchone()
      if res: return res
    except:
      print("Ошибка чтения из БД")
    return []