from flask import Flask, abort, flash, make_response, redirect, render_template, g, request, url_for
import psycopg2
import os
from admin.admin import admin

from DataBase import DataBase

app = Flask(__name__)

app.config['SECRET_KEY'] = 'home56172'

hesh = [{"title": "Главная", "url": "/"}, {"title": "Книги", "url": "/books"}, {"title": "Найти по тегу", "url": "/show_tags/0"}]

app.register_blueprint(admin, url_prefix='/admin')

def connect_db():
  conn = psycopg2.connect(
        host="localhost",
        database="library_system",
        user="user_1",
        password="1234")
  return conn

def create_db():
  db = connect_db()
  f = open('./instance/db.sql', 'r', encoding='utf-8')
  # with app.open_instance_resource('db.sql', mode = 'r') as f:
  db.cursor().execute(f.read())
  db.commit()
  db.close()

def get_db():
  if not hasattr(g, 'link_db'):
    g.link_db = connect_db()
  return g.link_db

dbase = None
@app.before_request
def before_request():
  global dbase
  db = get_db()
  dbase = DataBase(db)

@app.route("/")
def index():
  return render_template('index.html', title="Главная", menu=hesh)

@app.route("/books")
def books():
  _books = dbase.getBooks()
  used_books = []
  for b in _books:
    author = dbase.getAuthorsOfBook(b[0])
    used_books.append(b + author[0])
  return render_template('books.html', title="Книги", menu=hesh, books = used_books)

@app.route("/download/<book_id>")
def download(book_id):
  book = dbase.getBook(book_id)
  print(book)
  current_path = os.getcwd()
  download_name = book[1].lower().replace(" ", "_") + ".pdf"
  if (book[5]):
    f = open('code.txt', "wb")
    f.write(book[5].tobytes())

    # file = open(current_path+"/"+download_name, 'wb')
    dir_spl  = current_path.split('\\')
    dir = "C:/Users/" + dir_spl[2] + "/Downloads"
    file = open(dir + "/" + download_name, 'wb')
    for line in open('code.txt', 'rb').readlines():
      file.write(line)
    file.close()

  _books = dbase.getBooks()
  if (book[5] and file):
    flash("Файл " + download_name + " сохранён в " + dir, "success")
  else:
    flash("Файл не может быть скачан", "error")
  if not book:
    abort(404)
  return redirect (url_for('show_card', book_id=book_id))

@app.route("/book_image/<book_id>")
def book_image(book_id):
  img = dbase.getBookImage(book_id)
  if img:
    img = img.tobytes()

  if img == None:
    img = open('./static/images/default.jpg', "rb")
    img = img.read()
    
  
  h = make_response(img)
  h.headers['Content-Type'] = 'image/jpg'
  return h

@app.route("/show_card/<book_id>")
def show_card(book_id):
  _book = dbase.getBook(book_id)
  book_tags = dbase.getTagsOfBook(book_id)
  all_tags = dbase.getAllTags()
  tags = []
  for t in book_tags:
    for t2 in all_tags:
      if(t[1] == t2[0]):
        tags.append(t2)
  authors = dbase.getAuthorsOfBook(book_id)
  return render_template('book_card.html', menu = hesh, title="Информация о книге", book = _book, tags = tags, authors = authors, len = len(authors))

@app.route("/show_image/<book_id>")
def show_image(book_id):
  return book_image(book_id)


@app.route("/show_tags_1", methods = ["POST", "GET"])
def show_tags_1():
  tag_id = request.form.get('tag_id')
  all_tags = dbase.getAllTags()
  books_1 = []
  if (int(tag_id) == 0):
    books_1 = dbase.getBooks()
  return redirect(url_for('show_tags', tag_id=tag_id))

@app.route("/show_tags/<tag_id>")
def show_tags(tag_id):
  all_tags = dbase.getAllTags()
  tag = dbase.getTag(tag_id)
  books_1 = []
  if (int(tag_id) == 0):
    books_1 = dbase.getBooks()
  else:
    books_1 = dbase.getBooksByTag(tag_id)
  books_2 = []
  for b in books_1:
    authors = dbase.getAuthorsOfBook(b[0])
    books_2.append(b + authors[0])
  print (books_2[0])
  return render_template('find_by_tag.html', menu = hesh, title="Найти по тегу", tags = all_tags, books = books_2, tag_id = tag_id, tag = tag)

# comment to create db
if __name__ == "__main__":
  app.run(debug = True)

# umcomment to create db
# create_db()