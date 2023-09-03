DROP TABLE IF EXISTS dmel_books;
DROP TABLE IF EXISTS dmel_book_tags;
DROP TABLE IF EXISTS dmel_tags;
DROP TABLE IF EXISTS dmel_book_authors;
DROP TABLE IF EXISTS dmel_authors;

CREATE TABLE dmel_books (id serial PRIMARY KEY,
                         title varchar (150) NOT NULL,
                         year integer NOT NULL,
                         num_pg integer NOT NULL,
                         discription varchar (500) NOT NULL,
                         file bytea DEFAULT NULL);       
                                

CREATE TABLE dmel_tags (id serial PRIMARY KEY,
                        tag varchar (150) NOT NULL);
                    

CREATE TABLE dmel_authors (id serial PRIMARY KEY,
                           author varchar (150) NOT NULL);
                                  

CREATE TABLE dmel_book_authors (id serial PRIMARY KEY,
                                author_id integer NOT NULL,
                                book_id integer NOT NULL);
                                  

CREATE TABLE dmel_book_tags (id serial PRIMARY KEY,
                             tag_id integer NOT NULL,
                             book_id integer NOT NULL);
                                  
                                  

