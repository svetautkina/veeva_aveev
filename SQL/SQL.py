import sqlite3
from datetime import datetime


def create_connection():
    """Создает подключение к базе данных"""
    try:
        connection = sqlite3.connect('telegram.db')
        connection.execute("PRAGMA foreign_keys = ON")
        print("Подключение к базе данных успешно установлено!")
        return connection
    except sqlite3.Error as error:
        print(f"Ошибка при подключении к базе данных: {error}")
        return None


def create_tables(connection):
    """Создает таблицы для пользователей и сообщений"""
    try:
        cursor = connection.cursor()

        user_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            register_data DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """

        messages_table_sql = """
        CREATE TABLE IF NOT EXISTS user_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        """

        cursor.execute(user_table_sql)
        cursor.execute(messages_table_sql)
        connection.commit()
        print("Таблицы успешно созданы!")
    except sqlite3.Error as error:
        print(f"Ошибка при создании таблицы {error}")


def user_exist(connection, user_id):
    """Проверяет существование пользователя в таблице users"""
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user_id,))
    count = cursor.fetchone()[0]
    return count > 0


def add_user(connection, user_id, username, first_name):
    """Добавляет нового пользователя в таблицу users"""
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
            (user_id, username, first_name)
        )
        connection.commit()
        print(f"Пользователь {user_id} добавлен в таблицу users!")
    except sqlite3.Error as error:
        print(f"Ошибка при добавлении пользователя {error}")


def add_message_with_user_check(connection, user_id, username, first_name, message_text):
    """Добавляет сообщение с предварительной проверкой пользователя"""
    try:
        if not user_exist(connection, user_id):
            add_user(connection, user_id, username, first_name)

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO user_messages (user_id, message) VALUES (?, ?)",
            (user_id, message_text)
        )
        connection.commit()
        print(f"Сообщение от пользователя {user_id} добавлено!")
    except sqlite3.Error as error:
        print(f"Ошибка при добавлении сообщения {error}")


def get_user_statistics(connection, user_id):
    """Получает статистику пользователя"""
    try:
        cursor = connection.cursor()
        stats_sql = """
        SELECT
            COUNT(*),
            MIN(timestamp) as first_message_time,
            MAX(timestamp) as last_message_time
        FROM user_messages
        WHERE user_id = ?
        """
        cursor.execute(stats_sql, (user_id,))
        results = cursor.fetchone()

        statistics = {
            'user_id': user_id,
            'total_messages': results[0],
            'first_message_time': results[1],
            'last_message_time': results[2],
        }
        return statistics
    except sqlite3.Error as error:
        print(f"Ошибка при получении статистики {error}")
        return None


if __name__ == "__main__":
    print("Начинаем расширенную демонстрацию работы с базой данных...")
    conn = create_connection()

    if conn:
        create_tables(conn)

        print("\n---Добавление сообщения с проверкой пользователей---")
        add_message_with_user_check(conn, 123456, "ivan_petrov", "Иван", "Привет, это мое первое сообщение!")
        add_message_with_user_check(conn, 123456, "ivan_petrov", "Иван", "Как работает этот бот?")
        add_message_with_user_check(conn, 789012, "maria_sidorova", "Мария", "Здравствуйте, я новый пользователь")
        add_message_with_user_check(conn, 123456, "ivan_petrov", "Иван", "Спасибо за помощь!")

        print("\n---Статистика пользователя 123456---")
        stats = get_user_statistics(conn, 123456)
        if stats:
            print(f"Статистика пользователя {stats['user_id']}")
            print(f"Всего сообщений: {stats['total_messages']}")
            print(f"Первое сообщение: {stats['first_message_time']}")
            print(f"Последнее сообщение: {stats['last_message_time']}")

        conn.close()
        print("\nДемонстрация завершена! Подключение к базе данных закрыто.")
