import os
from flask import make_response
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="library_system",
        user="user_1",
        password="1234")

print (conn)

# Open a cursor to perform database operations
cur = conn.cursor()

path_file="./Melnik_1308_2.0.pdf"
f = open(path_file,'rb')
dat = f.read()
binary_file = psycopg2.Binary(dat)

path_img="./static/images/9.jpeg"
f = open(path_img,'rb')
dat = f.read()
binary_img = psycopg2.Binary(dat)
cur.execute('INSERT INTO dmel_books (author, title, year, num_pg, discription, file, image)'
            'VALUES (%s, %s, %s, %s, %s, %s, %s)',
            ('text', 'Charles Dickens', 1997, 320, "discription", binary_file, binary_img)
            )
conn.commit()
# cur.execute (f"UPDATE dmel_books SET file = '{binary}' WHERE id=1'")


print ("made")
cur.close()
conn.close()