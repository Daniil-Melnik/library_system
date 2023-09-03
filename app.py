from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
import os
import string

app = Flask(__name__)

app.config['SECRET_KEY'] = 'home56172'

hesh = [{"title": "Главная", "url": "/"}, {"title": "Книги", "url": "/books"}, {"title": "Авторы", "url": "/authors"}]

@app.route("/")
def index():
  return render_template('index.html', title="Главная", menu=hesh)

@app.route("/books")
def books():
  return render_template('index.html', title="Книги", menu=hesh)

@app.route("/authors")
def authors():
  return render_template('index.html', title="Авторы", menu=hesh)

if __name__ == "__main__":
  app.run(debug = True)