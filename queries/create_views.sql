-- Представление с информацией о книгах и их жанрах
CREATE VIEW IF NOT EXISTS books_with_genres AS
SELECT
    b.book_id,
    b.title,
    b.author,
    b.year_published,
    g.genre_name
FROM books_list AS b
JOIN genre AS g ON b.genre_id = g.genre_id;

-- Представление с подробной информацией о выдаче книг читателям
CREATE VIEW IF NOT EXISTS issuance_details AS
SELECT
    bi.issuance_id,
    b.title AS book_title,
    r.name AS reader_name,
    bi.issue_date,
    bi.return_date,
    DATEDIFF('day', bi.issue_date, bi.return_date) AS days_held
FROM book_issuance AS bi
JOIN books_list AS b ON bi.book_id = b.book_id
JOIN readers AS r ON bi.reader_id = r.reader_id;

-- Представление с отзывами читателей на книги
CREATE VIEW IF NOT EXISTS reviews_details AS
SELECT
    br.review_id,
    b.title AS book_title,
    r.name AS reader_name,
    br.rating,
    br.review_text
FROM book_reviews AS br
JOIN books_list AS b ON br.book_id = b.book_id
JOIN readers AS r ON br.reader_id = r.reader_id;