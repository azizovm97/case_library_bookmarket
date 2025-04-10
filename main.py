import streamlit as st
import plotly.express as px
from db import get_dataframe

st.title("📚 Library Dashboard")

# Загрузка данных
books_df = get_dataframe('SELECT * FROM books_list')
genre_df = get_dataframe('SELECT * FROM genre')
issuance_df = get_dataframe('SELECT * FROM book_issuance')
reviews_df = get_dataframe('SELECT * FROM book_reviews')

# Объединение данных
books_with_genre = get_dataframe('''
SELECT b.*, g.genre_name
FROM books_list b JOIN genre g ON b.genre_id = g.genre_id
''')

# Фильтры
selected_genre = st.selectbox("Выбрать жанр", ['Все'] + genre_df['genre_name'].tolist())

if selected_genre != 'Все':
    books_with_genre = books_with_genre[books_with_genre['genre_name'] == selected_genre]

# Диаграммы
fig_books_by_genre = px.histogram(books_with_genre, x='genre_name', title='Количество книг по жанрам')
st.plotly_chart(fig_books_by_genre)

fig_books_by_year = px.histogram(books_with_genre, x='year_published', title='Распределение книг по годам публикации')
st.plotly_chart(fig_books_by_year)

fig_top_authors = px.bar(books_with_genre['author'].value_counts().head(10),
                         title='Топ-10 авторов по количеству книг')
st.plotly_chart(fig_top_authors)

ratings_df = get_dataframe('''
SELECT b.title, AVG(r.rating) AS avg_rating
FROM book_reviews r JOIN books_list b ON r.book_id = b.book_id
GROUP BY b.title
ORDER BY avg_rating DESC LIMIT 10
''')

fig_top_rated = px.bar(ratings_df, x='avg_rating', y='title', orientation='h', title='Топ-10 книг по рейтингу')
st.plotly_chart(fig_top_rated)