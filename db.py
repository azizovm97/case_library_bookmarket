import duckdb
import pandas as pd

def get_dataframe(query: str) -> pd.DataFrame:
    """
    Выполняет SQL-запрос к базе данных и возвращает результат в виде датафрейма.
    """
    with duckdb.connect('my.db') as con:
        df = con.execute(query).df()
    return df

# Пример использования функции:
if __name__ == '__main__':
    query = 'SELECT * FROM books_list;'
    print(get_dataframe(query).head())