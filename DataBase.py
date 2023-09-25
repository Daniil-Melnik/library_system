from flask import url_for
import psycopg2

import traceback
from psycopg2 import errors

InFailedSqlTransaction = errors.lookup('25P02')


class DataBase:
  def __init__(self, db):
    self.__db = db
    self.__cur = db.cursor()
  
  def getBooks(self):
    sql = '''SELECT * FROM dmel_books ORDER BY title'''
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

  def addBook(self, author, title, num_pg, year, discription, image, file, is_open):
    try:
      dat = file.read()
      binary_file = psycopg2.Binary(dat)

      dat = image.read()
      binary_img = psycopg2.Binary(dat)
      self.__cur.execute('INSERT INTO dmel_books (author, title, year, num_pg, discription, file, image, is_open)'
                  'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                  (author, title, year, num_pg, discription, binary_file, binary_img, is_open)
                  )

      self.__db.commit()
      return True
    except :
      print("Ошибка добавления в БД")

  def deleteBook(self, book_id):
    try:
      self.__cur.execute("DELETE FROM dmel_books WHERE id = %s", [book_id])
      self.__db.commit()
      return True
    except InFailedSqlTransaction:
                traceback.print_exc()
                self._cr.rollback()
                pass
  def updateBook(self, book_id, author, title, num_pg, year, discription, is_open):
    try:
      self.__cur.execute('UPDATE dmel_books SET title = %s WHERE id = %s ', (title, book_id))
      self.__cur.execute('UPDATE dmel_books SET year = %s WHERE id = %s ', (year, book_id))
      self.__cur.execute('UPDATE dmel_books SET num_pg = %s WHERE id = %s ', (num_pg, book_id))
      self.__cur.execute('UPDATE dmel_books SET discription = %s WHERE id = %s ', (discription, book_id))
      self.__cur.execute('UPDATE dmel_books SET is_open = %s WHERE id = %s ', (is_open, book_id))
      self.__db.commit()
      return True
    except :
      print("Ошибка изменения в БД")
  
  def updateFileImg(self, book_id, image):
    try:
      dat = image.read()
      binary_img = psycopg2.Binary(dat)
      self.__cur.execute('UPDATE dmel_books SET image = %s WHERE id = %s ', (binary_img, book_id))
      self.__db.commit()
      return True
    except InFailedSqlTransaction:
                traceback.print_exc()
                self._cr.rollback()
                pass
    
  def updateFilePdf(self, book_id, file):
    try:
      dat = file.read()
      binary_file = psycopg2.Binary(dat)
      self.__cur.execute('UPDATE dmel_books SET file = %s WHERE id = %s ', (binary_file, book_id))
      self.__db.commit()
      return True
    except InFailedSqlTransaction:
                traceback.print_exc()
                self._cr.rollback()
                pass
  
  def getTagsOfBook(self, book_id):
    try:
      self.__cur.execute(f"SELECT * FROM dmel_book_tags WHERE book_id = '{book_id}'")
      books = self.__cur.fetchall()
      self.__db.commit()
      return books
    except InFailedSqlTransaction:
                traceback.print_exc()
                self._cr.rollback()
                pass
    
  def getAllTags(self):
    try:
      self.__cur.execute(f"SELECT * FROM dmel_tags ORDER BY id")
      tags = self.__cur.fetchall()
      self.__db.commit()
      return tags
    except InFailedSqlTransaction:
                traceback.print_exc()
                self._cr.rollback()
                pass
  def getTag(self, tag_id):
    try:
      self.__cur.execute("SELECT * FROM dmel_tags WHERE id = %s", [tag_id])
      tag = self.__cur.fetchone()
      self.__db.commit()
      return tag
    except InFailedSqlTransaction:
                traceback.print_exc()
                self._cr.rollback()
                pass

  def getBooksByTag(self, tag_id):
    try:
      self.__cur.execute("SELECT * FROM dmel_book_tags WHERE tag_id = %s", [tag_id])
      tags = self.__cur.fetchall()
      self.__db.commit()

      tag_ids = []
      for tag in tags:
          if (int(tag[1]) == int(tag_id)):
              tag_ids.append(tag[2])

      self.__cur.execute("SELECT * FROM dmel_books")
      books = self.__cur.fetchall()
      self.__db.commit()

      used_books = []

      for book in books:
          if (int(book[0]) in tag_ids):
              used_books.append(book)
      return used_books
    except InFailedSqlTransaction:
                traceback.print_exc()
                self._cr.rollback()
                pass
  
  def addTag(self, tag):
    try:
      self.__cur.execute('INSERT INTO dmel_tags (tag)'
                  'VALUES (%s)',
                  (tag,)
                  )
      self.__db.commit()
      return True
    except InFailedSqlTransaction:
                traceback.print_exc()
                self._cr.rollback()
                pass
    
  def deleteTag(self, tag_id):
    try:
      self.__cur.execute("DELETE FROM dmel_tags WHERE id = %s", [tag_id])
      self.__db.commit()
    except InFailedSqlTransaction:
                traceback.print_exc()
                self._cr.rollback()
                pass
    
  def deleteTagBook(self, book_id, tag_id):
    try:
      self.__cur.execute("DELETE FROM dmel_book_tags WHERE book_id = %s AND tag_id = %s", [book_id, tag_id])
      self.__db.commit()
    except InFailedSqlTransaction:
                traceback.print_exc()
                self._cr.rollback()
                pass
    
  def addTagBook(self, book_id, tag_id):
    try:
      self.__cur.execute('INSERT INTO dmel_book_tags (book_id, tag_id)'
                  'VALUES (%s, %s)',
                  (book_id, tag_id)
                  )
      self.__db.commit()
      return True
    except InFailedSqlTransaction:
                traceback.print_exc()
                self._cr.rollback()
                pass
  
  def getAllAuthors(self):
    try:
      self.__cur.execute(f"SELECT id, name, sec_name, sourname FROM dmel_authors ORDER BY sourname")
      authors = self.__cur.fetchall()
      return authors
    except InFailedSqlTransaction:
                traceback.print_exc()
                self._cr.rollback()
                pass

  def addAuthor(self, name, sourname, sec_name):
    try:
      self.__cur.execute('INSERT INTO dmel_authors (name, sourname, sec_name)'
                  'VALUES (%s, %s, %s)',
                  (name, sourname, sec_name)
                  )
      self.__db.commit()
      return True
    except InFailedSqlTransaction:
                traceback.print_exc()
                self._cr.rollback()
                pass
    
  def deleteAuthor(self, author_id):
    try:
      self.__cur.execute("DELETE FROM dmel_authors WHERE id = %s", [author_id])
      self.__db.commit()
    except InFailedSqlTransaction:
                traceback.print_exc()
                self._cr.rollback()
                pass
  def addBookAuthor(self, book_id, author_id):
      try:
        self.__cur.execute('INSERT INTO dmel_book_authors (book_id, author_id)'
                    'VALUES (%s, %s)',
                    (book_id, author_id)
                    )
        self.__db.commit()
        return True
      except InFailedSqlTransaction:
                  traceback.print_exc()
                  self._cr.rollback()
                  pass

  def getAuthorsOfBook(self, book_id):
    try:
      self.__cur.execute(f"SELECT * FROM dmel_book_authors WHERE book_id = '{book_id}'")
      authors = self.__cur.fetchall()
      self.__db.commit()
      all_authors = self.getAllAuthors()
      used_authors = []
      for a in all_authors:
          for b in authors:
              if (int(a[0]) == int(b[1])):
                  used_authors.append(a)
      return used_authors
    except InFailedSqlTransaction:
                traceback.print_exc()
                self._cr.rollback()
                pass
    
  def deleteAuthorBook(self, book_id, author_id):
    try:
      self.__cur.execute("DELETE FROM dmel_book_authors WHERE book_id = %s AND author_id = %s", [book_id, author_id])
      self.__db.commit()
    except InFailedSqlTransaction:
                traceback.print_exc()
                self._cr.rollback()
                pass
    