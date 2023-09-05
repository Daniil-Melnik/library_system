DROP TABLE IF EXISTS dmel_books;
DROP TABLE IF EXISTS dmel_book_tags;
DROP TABLE IF EXISTS dmel_tags;

CREATE TABLE dmel_books (id serial PRIMARY KEY,
                        author varchar (150) NOT NULL,
                        title varchar (150) NOT NULL,
                        year integer NOT NULL,
                        num_pg integer NOT NULL,
                        discription varchar (500) NOT NULL,
                        file bytea DEFAULT NULL,
                        image bytea DEFAULT NULL,
                        is_open integer DEFAULT 0);       
                                

CREATE TABLE dmel_tags (id serial PRIMARY KEY,
                        tag varchar (150) NOT NULL);
                                 

CREATE TABLE dmel_book_tags (id serial PRIMARY KEY,
                             tag_id integer NOT NULL,
                             book_id integer NOT NULL);

INSERT INTO dmel_books (title, author, year, num_pg, discription, is_open, file, image)
VALUES ('Портрет Дориана Грея', 'Уайльд Оскар', 2019, 320,'Портрет молого человаека по имени Дориан Грей', 1, NULL, NULL),
    ('Овод', 'Войнич Э. Л.', 2017, 350,'Одно из самых известный произведений, которое не оставит читателя равнодушным', 1, NULL, NULL),
	('1984 (новый перевод)', 'Оруэлл Д.', 2020, 322,'Классика американской антиутопии', 1, NULL, NULL),
	('Маленькие женщины', 'Олкотт Луиза Мэй',2021, 384,'Известный роман известной писательницы о сильных женщинах', 1, NULL, NULL),
    ('В окопах Сталинграда', 'Некрасов В. П.',2019, 314,'Произведение об одной из самых важный и кровопролитных битв в Великой Отечественной войне', 1, NULL, NULL),
	('Повелитель мух', 'Голдинг Уильям Джеральд',2020, 320,'Проза об одичавших на острове', 1, NULL, NULL);

INSERT INTO dmel_tags (tag)
VALUES ('Рассказ'),
	('Очерк'),
	('Роман'),
    ('Лейтенантская проза'),
    ('Антиутопия'),
    ('Уальд'),
    ('19 век'),
    ('Новые издания');

INSERT INTO dmel_book_tags (tag_id, book_id)
VALUES (3, 1),
	(8, 1),
	(7, 1),
    (8, 2),
    (3, 2),
    (7, 2),
    (3, 5),
    (4, 5);

                                  
                                  

