import sqlite3
from threading import RLock


class UserInfoDatabase:
    def __init__(self, path: str):
        self.__path = path
        with sqlite3.connect(self.__path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER, question_id INTEGER)''')
            conn.commit()

        self.__lock = RLock()

    def get(self, user_id: int) -> int:
        with self.__lock:
            with sqlite3.connect(self.__path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id, ))
                row = cursor.fetchone()
                return row[1]

    def update_user(self, user_id: int):
        with self.__lock:
            with sqlite3.connect(self.__path) as conn:
                conn.execute('INSERT or REPLACE into users (user_id, question_id) values (?, ?)',
                                    (user_id, 0))
                conn.commit()
