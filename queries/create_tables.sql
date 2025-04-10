CREATE TABLE IF NOT EXISTS books_list (
    book_id INTEGER PRIMARY KEY,
    title VARCHAR,
    author VARCHAR,
    year_published INTEGER,
    genre_id INTEGER
);

CREATE TABLE IF NOT EXISTS readers (
    reader_id INTEGER PRIMARY KEY,
    name VARCHAR,
    email VARCHAR,
    registered_date DATE
);

CREATE TABLE IF NOT EXISTS book_issuance (
    issuance_id INTEGER PRIMARY KEY,
    book_id INTEGER,
    reader_id INTEGER,
    issue_date DATE,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books_list(book_id),
    FOREIGN KEY (reader_id) REFERENCES readers(reader_id)
);

CREATE TABLE IF NOT EXISTS book_reviews (
    review_id INTEGER PRIMARY KEY,
    book_id INTEGER,
    reader_id INTEGER,
    rating INTEGER,
    review_text VARCHAR,
    FOREIGN KEY (book_id) REFERENCES books_list(book_id),
    FOREIGN KEY (reader_id) REFERENCES readers(reader_id)
);

CREATE TABLE IF NOT EXISTS genre (
    genre_id INTEGER PRIMARY KEY,
    genre_name VARCHAR
);
