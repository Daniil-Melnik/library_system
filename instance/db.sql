DROP TABLE IF EXISTS dmel_books;
DROP TABLE IF EXISTS dmel_book_tags;
DROP TABLE IF EXISTS dmel_tags;
DROP TABLE IF EXISTS dmel_book_authors;
DROP TABLE IF EXISTS dmel_authors;

CREATE TABLE dmel_books (id serial PRIMARY KEY,
                        author varchar (150) NOT NULL,
                        title varchar (150) NOT NULL,
                        year integer NOT NULL,
                        num_pg integer NOT NULL,
                        discription varchar (500) NOT NULL,
                        file bytea DEFAULT NULL);       
                                

CREATE TABLE dmel_tags (id serial PRIMARY KEY,
                        tag varchar (150) NOT NULL);
                                 

CREATE TABLE dmel_book_tags (id serial PRIMARY KEY,
                             tag_id integer NOT NULL,
                             book_id integer NOT NULL);

INSERT INTO dmel_books (title, author, year, num_pg, discription, file)
VALUES ('Портрет Дориана Грея', 'Уайльд Оскар', 2019, 320,'Портрет молого человаека по имени Дориан Грей', NULL),
	('1984 (новый перевод)', 'Оруэлл Д.', 2020, 322,'Классика американской антиутопии', NULL),
	('Маленькие женщины', 'Олкотт Луиза Мэй',2021, 384,'Известный роман известной писательницы о сильных женщинах', NULL),
	('Повелитель мух', 'Голдинг Уильям Джеральд',2020, 320,'Проза об одичавших на острове', NULL);
                                  
                                  

