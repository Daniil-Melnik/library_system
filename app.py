from flask import Flask, abort, flash, make_response, render_template, g
import psycopg2
import os
from admin.admin import admin

from DataBase import DataBase

app = Flask(__name__)

app.config['SECRET_KEY'] = 'home56172'

hesh = [{"title": "Главная", "url": "/"}, {"title": "Книги", "url": "/books"}]

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
  print (_books)
  return render_template('books.html', title="Книги", menu=hesh, books = _books)

@app.route("/download/<book_id>/<template>")
def download(book_id, template):
  book = dbase.getBook(book_id)
  current_path = os.getcwd()
  download_name = book[2].lower().replace(" ", "_") + ".pdf"

  f = open('code.txt', "wb")
  f.write(book[6].tobytes())

  # file = open(current_path+"/"+download_name, 'wb')
  dir_spl  = current_path.split('\\')
  dir = "C:/Users/" + dir_spl[2] + "/Downloads"
  file = open(dir + "/" + download_name, 'wb')
  for line in open('code.txt', 'rb').readlines():
    file.write(line)
  file.close()

  _books = dbase.getBooks()
  if file:
    flash("Файл " + download_name + " сохранён в " + dir, "success")
  if not book:
    abort(404)
  return render_template(template, menu = hesh, title="Книги", books=_books)

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
  return render_template('book_card.html', menu = hesh, title="Книги", book = _book)


if __name__ == "__main__":
  app.run(debug = True)

# create_db()