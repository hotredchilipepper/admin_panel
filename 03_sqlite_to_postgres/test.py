import sqlite3
from contextlib import contextmanager  


# Задаём путь к файлу с базой данных
db_path = 'db.sqlite'

@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn


db_path = 'db.sqlite'
with conn_context(db_path) as conn:
    curs = conn.cursor()
    curs.execute("SELECT * FROM person;")
    data = curs.fetchall()
    print(dict(data[0]))
