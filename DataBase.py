from flask import url_for
import psycopg2

import traceback  # Just to show the full traceback
from psycopg2 import errors

InFailedSqlTransaction = errors.lookup('25P02')


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
  
  def getBookImage(self, book_id):
    img = None
    try:
      self.__cur.execute(f"SELECT * FROM dmel_books WHERE id = '{book_id}' LIMIT 1")
      res = self.__cur.fetchone()
      print (res)
      img = res[7]
      if img: return img
    except :
      print("Ошибка чтения из БД")

  def addBook(self, author, title, num_pg, year, discription, image, file):
    try:
      dat = file.read()
      binary_file = psycopg2.Binary(dat)

      dat = image.read()
      binary_img = psycopg2.Binary(dat)
      self.__cur.execute('INSERT INTO dmel_books (author, title, year, num_pg, discription, file, image)'
                  'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                  (author, title, year, num_pg, discription, binary_file, binary_img)
                  )
      print("OK1")
      self.__db.commit()
      print("OK2")
      return True
    except :
      print("Ошибка добавления в БД")

  def deleteBook(self, book_id):
    try:
      print(book_id)
      self.__cur.execute("DELETE FROM dmel_books WHERE id = %s", [book_id])
      self.__db.commit()
      return True
    except InFailedSqlTransaction:
                traceback.print_exc()
                self._cr.rollback()
                pass