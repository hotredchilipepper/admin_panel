import sqlite3
from contextlib import contextmanager  


# Задаём путь к файлу с базой данных
db_path = 'db.sqlite'

@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn # С конструкцией yield вы познакомитесь в следующем модуле 
    # Пока воспринимайте её как return, после которого код может продолжить выполняться дальше
    # Формируем запрос. Внутри execute находится обычный SQL запрос


db_path = 'db.sqlite'
with conn_context(db_path) as conn:
    curs = conn.cursor()
    curs.execute("SELECT * FROM person;")
    data = curs.fetchall()
    print(dict(data[0]))
