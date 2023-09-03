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

path="./Melnik_1308_2.0.pdf"
f = open(path,'rb')
dat = f.read()
binary = psycopg2.Binary(dat)

cur.execute('INSERT INTO dmel_books (author, title, year, num_pg, discription, file)'
            'VALUES (%s, %s, %s, %s, %s, %s)',
            ('text', 'Charles Dickens', 1997, 320, "discription", binary)
            )
conn.commit()
# cur.execute (f"UPDATE dmel_books SET file = '{binary}' WHERE id=1'")


print ("made")
cur.close()
conn.close()