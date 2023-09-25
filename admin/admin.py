import os
from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for, g
import psycopg2

from DataBase import DataBase

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

_hesh = [
        {"url": 'index', "title": 'Витрина'},
        {"url": '.showList', "title": 'Книги'},
        {"url": '.show_tags', "title": 'Теги'},
        {"url": '.show_authors', "title": 'Авторы'},
        {"url": '.addBook_form', "title": 'Добавить книгу'}
         ]

def connect_db():
  conn = psycopg2.connect(
        host="localhost",
        database="library_system",
        user="user_1",
        password="1234")
  return conn

def get_db():
  if not hasattr(g, 'link_db'):
    g.link_db = connect_db()
  return g.link_db

dbase = None
@admin.before_request
def before_request():
  global dbase
  db = get_db()
  dbase = DataBase(db)


@admin.teardown_request
def teardown_request(request):
    global dbase
    dbase = None
    return request

@admin.route('/')
def index():
  if not is_logged():
    return redirect(url_for('.login'))
  return render_template("admin/index.html", hesh = _hesh, title = "Админ-панель")

@admin.route('/login', methods = ["POST", "GET"])
def login():
  if is_logged():
    return redirect(url_for('.index'))
  
  if request.method == 'POST':
    if request.form['user'] == "admin" and request.form['psw'] == "12345":
      login_admin()
      return redirect(url_for('.index'))
    else:
      flash("Неверная пара логин-пароль")
  return render_template('admin/login.html', title = 'Админ-панель')

@admin.route('/logout', methods = ["POST", "GET"])
def logout():
  if request.method == 'POST':
    if not is_logged():
      return redirect(url_for('.login'))
  logout_admin()
  return redirect(url_for('.login'))

@admin.route('/book_list')
def showList():
  if not is_logged():
    return redirect(url_for('.login'))
  books = dbase.getBooks()
  return render_template('admin/book_list.html', title = "Список книг", hesh = _hesh, books = books)

@admin.route('/add_book', methods = ["POST", "GET"])
def add_book():
  
  if request.method == "POST":
    val = 1 if request.form.get('is_open') else 0
    dbase.addBook(request.form['author'],request.form['title'],request.form['num_pg'], request.form['year'], request.form['discr'], request.files['image'], request.files['file'], val)
    return redirect(url_for('admin.showList'))

@admin.route('/add_book_form')
def addBook_form():
  if not is_logged():
    return redirect(url_for('.login'))
  books = dbase.getBooks()
  return render_template('admin/add_book.html', title = "Добавить книгу", hesh = _hesh, books = books)

@admin.route("/delete_book/<book_id>")
def delete_book(book_id):
  if not is_logged():
    return redirect(url_for('.login'))
  dbase.deleteBook(book_id)
  return redirect(url_for('admin.showList'))

@admin.route("/update_book_form/<book_id>")
def update_book_form(book_id):
  if not is_logged():
    return redirect(url_for('.login'))
  books = dbase.getBooks()
  book = dbase.getBook(book_id)
  return render_template('admin/update_book.html', title = "Редактирование", hesh = _hesh, books = books, book_id=book_id, book=book)

@admin.route("/update_book_file_form/<book_id>")
def update_book_file_form(book_id):
  if not is_logged():
    return redirect(url_for('.login'))
  books = dbase.getBooks()
  book = dbase.getBook(book_id)
  return render_template('admin/update_book_file.html', title = "Редактирование", hesh = _hesh, books = books, book_id=book_id, book=book)



@admin.route("/update_book/<book_id>", methods = ["POST", "GET"])
def update_book(book_id):
  if not is_logged():
    return redirect(url_for('.login'))
  if request.method == "POST":
    val = 1 if request.form.get('is_open') else 0

    dbase.updateBook(book_id, request.form['author'],request.form['title'],request.form['num_pg'], request.form['year'], request.form['discr'], val)
  books = dbase.getBooks()
  return redirect(url_for('admin.show_card', book_id=book_id))

@admin.route("/update_files_form/<book_id>")
def update_files_form(book_id):
  if not is_logged():
    return redirect(url_for('.login'))
  books = dbase.getBooks()
  book = dbase.getBook(book_id)
  return render_template('admin/update_files.html', title = "Редактирование", hesh = _hesh, books = books, book_id=book_id, book=book)

@admin.route("/update_files/<book_id>", methods = ["POST", "GET"])
def update_files(book_id):
  if not is_logged():
    return redirect(url_for('.login'))
  if request.method == "POST":
    dbase.updateFileImg(book_id, request.files['image'])
  return redirect(url_for('admin.show_card', book_id=book_id))

@admin.route("/update_book_file/<book_id>", methods = ["POST", "GET"])
def update_book_file(book_id):
  if not is_logged():
    return redirect(url_for('.login'))
  if request.method == "POST":
    dbase.updateFilePdf(book_id, request.files['file'])
  return redirect(url_for('admin.show_card', book_id=book_id))

@admin.route("/add_tag", methods = ["POST", "GET"])
def add_tag():
  if not is_logged():
    return redirect(url_for('.login'))
  if request.method == "POST":
    dbase.addTag(request.form['tag'])
  return redirect(url_for('admin.show_tags'))

@admin.route("/delete_tag/<tag_id>")
def delete_tag(tag_id):
  if not is_logged():
    return redirect(url_for('.login'))
  dbase.deleteTag(tag_id)
  return redirect(url_for('admin.show_tags'))

@admin.route("/show_card/<book_id>")
def show_card(book_id):
  if not is_logged():
    return redirect(url_for('.login'))
  _book = dbase.getBook(book_id)
  book_tags = dbase.getTagsOfBook(book_id)
  all_tags = dbase.getAllTags()
  tags = []
  authors = dbase.getAuthorsOfBook(book_id)
  for t in book_tags:
    for t2 in all_tags:
      if(t[1] == t2[0]):
        tags.append(t2[1])
  return render_template('admin/book_card.html', hesh = _hesh, title="Информация о книге", book = _book, tags = tags, authors = authors, len = len(authors))

@admin.route("/download/<book_id>")
def download(book_id):
  if not is_logged():
    return redirect(url_for('.login'))
  book = dbase.getBook(book_id)
  current_path = os.getcwd()
  download_name = book[2].lower().replace(" ", "_") + ".pdf"

  f = open('code.txt', "wb")
  f.write(book[6].tobytes())

  dir_spl  = current_path.split('\\')
  dir = "C:/Users/" + dir_spl[2] + "/Downloads"
  file = open(dir + "/" + download_name, 'wb')
  for line in open('code.txt', 'rb').readlines():
    file.write(line)
  file.close()

  if file:
    flash("Файл " + download_name + " сохранён в " + dir, "success")
  if not book:
    abort(404)
  return redirect(url_for('admin.show_card', book_id=book_id))

@admin.route("/show_tags")
def show_tags():
  if not is_logged():
    return redirect(url_for('.login'))
  tags = dbase.getAllTags()
  return render_template('admin/tag_page.html', title = "Теги", hesh = _hesh,  tags = tags)

@admin.route("/update_tags/<book_id>")
def update_tags(book_id):
  if not is_logged():
    return redirect(url_for('.login'))
  _book = dbase.getBook(book_id)
  book_tags = dbase.getTagsOfBook(book_id)
  all_tags = dbase.getAllTags()
  tags = []
  unused_tags = []
  index_used_tags = []
  for t in book_tags:
    for t2 in all_tags:
      if(t[1] == t2[0]):
        tags.append(t2)
  for el in book_tags:
    index_used_tags.append(el[1])
  for i in range (len(all_tags)):
    if (all_tags[i][0] not in index_used_tags):
      unused_tags.append(all_tags[i])

  return render_template('admin/update_tags.html', hesh = _hesh, title="Редактирование тегов", book = _book, tags = tags, all_tags = unused_tags)


@admin.route("/delete_tag_book/<tag_id>/<book_id>")
def delete_tag_book(book_id, tag_id):
  if not is_logged():
    return redirect(url_for('.login'))
  dbase.deleteTagBook(book_id, tag_id)
  return redirect(url_for('admin.update_tags', book_id=book_id))

@admin.route("/add_tag_book/<book_id>", methods = ["POST", "GET"])
def add_tag_book(book_id):
  if not is_logged():
    return redirect(url_for('.login'))
  if request.method == "POST":
    book_id = book_id
    tag_id = request.form.get('tag_id')
    add_cond = True
    print (book_id)
    print (tag_id)
    for el in dbase.getTagsOfBook(book_id):
      if ((int(el[2]) == int(book_id)) and (int(el[1]) == int(tag_id))):
        add_cond=False
    if add_cond:
      dbase.addTagBook(book_id, tag_id)
  return redirect(url_for('admin.update_tags', book_id=book_id))

@admin.route("/show_authors")
def show_authors():
  if not is_logged():
    return redirect(url_for('.login'))
  authors = dbase.getAllAuthors()
  return render_template('admin/author_page.html', title = "Авторы", hesh = _hesh,  authors = authors)

@admin.route("/add_author", methods = ["POST", "GET"])
def add_author():
  if not is_logged():
    return redirect(url_for('.login'))
  if request.method == "POST":
    print (request.form['sec_name'])
    dbase.addAuthor(request.form['name'], request.form['sourname'], request.form['sec_name'])
  return redirect(url_for('admin.show_authors'))

@admin.route("/delete_author/<author_id>")
def delete_author(author_id):
  if not is_logged():
    return redirect(url_for('.login'))
  dbase.deleteAuthor(author_id)
  return redirect(url_for('admin.show_authors'))


@admin.route("/add_book_author_main")
def add_book_author_main():
  if not is_logged():
    return redirect(url_for('.login'))
  
  books = dbase.getBooks()
  authors = dbase.getAllAuthors()

  return render_template('admin/add_book_author.html', books = books, authors = authors, title = "Добавить книге автора", hesh = _hesh)

@admin.route("/add_book_author", methods = ["POST", "GET"])
def add_book_author():
  if not is_logged():
    return redirect(url_for('.login'))
  if request.method == "POST":
    dbase.addBookAuthor(request.form.get('book_id'), request.form.get('author_id'))
  return redirect(url_for('admin.add_book_author_main'))

@admin.route("/update_book_author/<book_id>")
def update_book_author(book_id):
  if not is_logged():
    return redirect(url_for('.login'))
  authors = dbase.getAuthorsOfBook(book_id)
  book = dbase.getBook(book_id)
  return render_template('admin/update_book_author.html', authors = authors, title = "Редактировать авторов книги", hesh = _hesh, book = book)

@admin.route("/delete_author_book/<author_id>/<book_id>")
def delete_auhor_book(book_id, author_id):
  if not is_logged():
    return redirect(url_for('.login'))
  dbase.deleteAuthorBook(book_id, author_id)
  return redirect(url_for('admin.update_book_author', book_id=book_id))

def login_admin():
  session['admin_logged'] = 1


def is_logged():
  return True if session.get('admin_logged') else False

def logout_admin():
  session.pop('admin_logged', None)
