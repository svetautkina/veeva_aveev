import sqlite3
from datetime import datetime
class BotDatabase:
    def __init__(self, db_name='telegram_bot.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    def create_tables(self):
        """Создает таблицы пользователей и сообщений"""
        cursor = self.conn.cursor()
        cursor.execute('''
          CREATE TABLE INF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            registration_date DATETIME DEFAUTLT CURRENT_TIMESTSMP
        )
    ''')
        cursor.execute('''
        CREATE TABLE INF NOT EXISTS user_name messages (
        id INTEGER PRIMARY KEY,
        message_text TEXT NOT NULL,
        timestamp DATETIME NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) 
        )
        ''')

        self.conn.commit()
        def user_exists(self, user_id):
            """Проверяет существование пользователя в базе данных"""
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            count = cursor.fetchone()[0]
            return count>0
        def add_user(self, user_id, username, first_name, registration_date):
            """Добовляет пользователя"""
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO user (user_id, username, first_name, registration_date) VALUES (?, ?, ?, ?)",
                (user_id, username, first_name, registration_date)
            )
            self.conn.commit()
        def save_message(self, user_id, message_text):
            """Сохраняет сообщение пользователя"""
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO messages (user_id, message_text) VALUES (?, ?)",
                (user_id, message_text)
            )
            self.conn.commit()



