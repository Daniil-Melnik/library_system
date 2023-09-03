from flask import Flask, render_template, g
import psycopg2

from DataBase import DataBase

app = Flask(__name__)

app.config['SECRET_KEY'] = 'home56172'

hesh = [{"title": "Главная", "url": "/"}, {"title": "Книги", "url": "/books"}, {"title": "Авторы", "url": "/authors"}]

def connect_db():
  conn = psycopg2.connect(
        host="localhost",
        database="library_system",
        user="user_1",
        password="1234")
  return conn

def create_db():
  db = connect_db()
  with app.open_instance_resource('db.sql', mode = 'r') as f:
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

@app.route("/authors")
def authors():
  return render_template('index.html', title="Авторы", menu=hesh)

if __name__ == "__main__":
  app.run(debug = True)