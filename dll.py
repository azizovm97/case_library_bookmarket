import os
import duckdb
import pandas as pd

# Удаление базы
if os.path.exists("my.db"):
    os.remove("my.db")

# Подключение к новой базе
con = duckdb.connect("my.db")

# Создание таблиц
with open("queries/create_tables.sql", "r", encoding="utf-8") as f:
    con.execute(f.read())

# Загрузка данных из Excel
xls = pd.ExcelFile("source/library_data.xlsx")
tables = ['books_list', 'readers', 'book_issuance', 'book_reviews', 'genre']

for table in tables:
    df = pd.read_excel(xls, sheet_name=table)
    con.register("temp_df", df)
    con.execute(f"INSERT INTO {table} SELECT * FROM temp_df")
    con.unregister("temp_df")

# Создание представлений
with open("queries/create_views.sql", "r", encoding="utf-8") as f:
    con.execute(f.read())

print("База успешно создана!")
con.close()