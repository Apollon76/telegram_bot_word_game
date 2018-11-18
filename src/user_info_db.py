import sqlite3
from threading import RLock

from src.user import User


class UserInfoDatabase:
    def __init__(self, path: str):
        self.__path = path
        with sqlite3.connect(self.__path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER, question_id INTEGER, points INTEGER)''')
            conn.commit()

        self.__lock = RLock()

    def get_user(self, user_id: int) -> User:
        with self.__lock:
            with sqlite3.connect(self.__path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id, ))
                row = cursor.fetchone()
                return User(*row)

    def create_user(self, user_id: int):
        with self.__lock:
            with sqlite3.connect(self.__path) as conn:
                conn.execute('INSERT or REPLACE into users (user_id, question_id, points) values (?, ?, ?)',
                                    (user_id, 0, 0))
                conn.commit()

    def update(self, user_id: int, value: int):
        with self.__lock:
            with sqlite3.connect(self.__path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
                row = cursor.fetchone()
                points = row[2]
                points += value
                cursor.execute(
                    'UPDATE users SET points = ? where user_id = ?',
                    (points, user_id)
                )
                conn.commit()
