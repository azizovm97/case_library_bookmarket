-- Запрос: Средний рейтинг каждой книги с количеством отзывов
SELECT
    book_title,
    ROUND(AVG(rating), 2) AS avg_rating,
    COUNT(review_id) AS reviews_count
FROM reviews_details
GROUP BY book_title
ORDER BY avg_rating DESC;

-- Запрос: ТОП-5 самых активных читателей по количеству прочитанных книг
SELECT
    reader_name,
    COUNT(issuance_id) AS books_read
FROM issuance_details
GROUP BY reader_name
ORDER BY books_read DESC
LIMIT 5;

-- Запрос: Среднее количество дней, на которое выдаётся каждая книга
SELECT
    book_title,
    ROUND(AVG(days_held), 1) AS avg_days_held
FROM issuance_details
GROUP BY book_title
ORDER BY avg_days_held DESC;

-- Запрос: Книги, опубликованные после среднего года публикации по всем книгам
SELECT
    title,
    author,
    year_published
FROM books_list
WHERE year_published > (
    SELECT AVG(year_published) FROM books_list
);

-- Запрос с оконной функцией: Рейтинг книг и ранг книг по среднему рейтингу
SELECT
    book_title,
    avg_rating,
    RANK() OVER (ORDER BY avg_rating DESC) AS rating_rank
FROM (
    SELECT
        book_title,
        ROUND(AVG(rating), 2) AS avg_rating
    FROM reviews_details
    GROUP BY book_title
) sub;