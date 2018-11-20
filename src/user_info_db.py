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
                conn.execute('INSERT or IGNORE into users (user_id, question_id, points) values (?, ?, ?)',
                             (user_id, 0, 0))
                conn.execute('UPDATE users SET question_id = ?, points = ? WHERE user_id = ?',
                             (0, 0, user_id))
                conn.commit()

    def update_points(self, user_id: int, value: int):
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

    def next_question(self, user_id: int):
        with self.__lock:
            user = self.get_user(user_id)
            with sqlite3.connect(self.__path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE users SET question_id = ? where user_id = ?',
                    (user.question_id + 1, user.id)
                )
                conn.commit()
