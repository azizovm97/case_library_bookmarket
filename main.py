import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_dataframe

st.set_page_config(page_title="Library Dashboard", layout="wide")
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

# Преобразование и очистка данных
books_with_genre['year_published'] = pd.to_numeric(books_with_genre['year_published'], errors='coerce')
books_with_genre = books_with_genre.dropna(subset=['year_published'])
books_with_genre['year_published'] = books_with_genre['year_published'].astype(int)

# Фильтры в боковой панели
st.sidebar.header("Фильтры")

# Фильтр по жанру
selected_genre = st.sidebar.selectbox("Жанр", ['Все'] + genre_df['genre_name'].tolist())
if selected_genre != 'Все':
    books_with_genre = books_with_genre[books_with_genre['genre_name'] == selected_genre]

# Фильтр по году публикации
min_year = books_with_genre['year_published'].min()
max_year = books_with_genre['year_published'].max()
year_range = st.sidebar.slider(
    "Год публикации",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1
)
books_with_genre = books_with_genre[
    (books_with_genre['year_published'] >= year_range[0]) &
    (books_with_genre['year_published'] <= year_range[1])
]

# Диаграмма: Количество книг по жанрам
fig_books_by_genre = px.histogram(
    books_with_genre,
    x='genre_name',
    title='Количество книг по жанрам'
)
st.plotly_chart(fig_books_by_genre, use_container_width=True)

# Диаграмма: Распределение книг по годам публикации
fig_books_by_year = px.histogram(
    books_with_genre,
    x='year_published',
    title='Распределение книг по годам публикации'
)
st.plotly_chart(fig_books_by_year, use_container_width=True)

# Диаграмма: Топ-10 авторов по количеству книг
top_authors = books_with_genre['author'].value_counts().head(10).reset_index()
top_authors.columns = ['author', 'count']
fig_top_authors = px.bar(
    top_authors,
    x='author',
    y='count',
    title='Топ-10 авторов по количеству книг'
)
st.plotly_chart(fig_top_authors, use_container_width=True)

# Диаграмма: Топ-10 книг по рейтингу
ratings_df = get_dataframe('''
SELECT b.title, AVG(r.rating) AS avg_rating
FROM book_reviews r JOIN books_list b ON r.book_id = b.book_id
GROUP BY b.title
ORDER BY avg_rating DESC LIMIT 10
''')
fig_top_rated = px.bar(
    ratings_df,
    x='avg_rating',
    y='title',
    orientation='h',
    title='Топ-10 книг по рейтингу'
)
st.plotly_chart(fig_top_rated, use_container_width=True)