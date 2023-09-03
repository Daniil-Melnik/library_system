from flask import Blueprint, flash, redirect, render_template, request, session, url_for, g
import psycopg2

from DataBase import DataBase

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

_hesh = [{"url": '.index', "title": 'Панель'}]

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

def login_admin():
  session['admin_logged'] = 1

def is_logged():
  return True if session.get('admin_logged') else False

def logout_admin():
  session.pop('admin_logged', None)
