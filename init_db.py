import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user="user_1",
        password="1234")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS dmel_books;')
cur.execute('DROP TABLE IF EXISTS dmel_book_tags;')
cur.execute('DROP TABLE IF EXISTS dmel_tags;')
cur.execute('DROP TABLE IF EXISTS dmel_book_authors;')
cur.execute('DROP TABLE IF EXISTS dmel_authors;')

cur.execute('CREATE TABLE dmel_books (id serial PRIMARY KEY,'
                                  'title varchar (150) NOT NULL,'
                                  'discription varchar (1500) NOT NULL,'
                                  'file bytea DEFAULT NULL);'          
                                 )

cur.execute('CREATE TABLE dmel_tags (id serial PRIMARY KEY,'
                                  'tag varchar (150) NOT NULL);'
                                  )

cur.execute('CREATE TABLE dmel_authors (id serial PRIMARY KEY,'
                                  'author varchar (150) NOT NULL);'
                                  )

cur.execute('CREATE TABLE dmel_book_authors (id serial PRIMARY KEY,'
                                  'author_id integer NOT NULL,'
                                  'book_id integer NOT NULL);'
                                  )

cur.execute('CREATE TABLE dmel_book_tags (id serial PRIMARY KEY,'
                                  'tag_id integer NOT NULL,'
                                  'book_id integer NOT NULL);'
                                  )

print ("made")

# Insert data into the table

# cur.execute('INSERT INTO dmel_books (title, discription, file)'
#             'VALUES (?, ?, NULL)',
#             ('C++++',
#              'Charles Dickens')
#             )

conn.commit()

cur.close()
conn.close()