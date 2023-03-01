import re
import sqlite3
import logging


def create_db(db_path: str):
    base = sqlite3.connect(db_path)
    base.cursor().execute(
        'CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, user_name TEXT, timezone INTEGER DEFAULT NULL)')
    base.commit()
    base.close()
    return logging.info('data-base.db created')


def add_user(db_path: str, user_id: int, user_name: str):
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(
        f'INSERT INTO users (user_id, user_name) VALUES ({user_id}, "{user_name}") ON CONFLICT(user_id) DO UPDATE SET user_name="{user_name}"')
    cursor.execute(
        f'CREATE TABLE IF NOT EXISTS user_{user_id} (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL, is_ready BOOLEAN NOT NULL DEFAULT 0, is_canceled BOOLEAN NOT NULL DEFAULT 0, important BOOLEAN NOT NULL DEFAULT 1)')
    cursor.execute(
        f'CREATE TABLE IF NOT EXISTS time_{user_id} (time TIME PRIMARY KEY, status BOOLEAN NOT NULL DEFAULT 1)')
    cursor.execute(
        f'INSERT INTO time_{user_id}  (time) VALUES ("09:00"), ("15:00"), ("21:00") ON CONFLICT(time) DO NOTHING')
    base.commit()
    base.close()
    return logging.info(f'table user_{user_id} created')


def read_user(db_path: str, user_id: int):
    user = dict()
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(
        f'SELECT * FROM users WHERE user_id = {user_id}')
    data = cursor.fetchall()[0]
    user['id'] = data[0]
    user['user_name'] = data[1]
    user['timezone'] = data[2]
    base.close()
    return user


def read_tasks(db_path: str, user_id: int):
    data_list = []
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(
        f'SELECT * FROM user_{user_id} WHERE is_ready = 0 AND is_canceled = 0')
    notify = cursor.fetchall()
    base.close()
    for n in notify:
        data_list.append([n[0], n[1], bool(n[2]), bool(n[3]), bool(n[4])])
    return data_list


def send_tasks(db_path: str, user_id: int):
    data_list = []
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(
        f'SELECT * FROM user_{user_id} WHERE is_ready = 0 AND is_canceled = 0 AND important = 1')
    notify = cursor.fetchall()
    base.close()
    for n in notify:
        data_list.append([n[0], n[1], bool(n[2]), bool(n[3]), bool(n[4])])
    return data_list


def read_history(db_path: str, user_id: int):
    data_list = []
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(
        f'SELECT * FROM user_{user_id} WHERE is_ready = 1 OR is_canceled = 1')
    notify = cursor.fetchall()
    base.close()
    for n in notify:
        data_list.append([n[0], n[1], bool(n[2]), bool(n[3])])
    return data_list


def read_times(db_path: str, user_id: int):
    data_list = []
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(f'SELECT * FROM time_{user_id} ORDER BY time')
    data = cursor.fetchall()
    base.close()
    for d in data:
        data_list.append([d[0], d[1]])
    return data_list


def read_users(db_path: str):
    data_list = []
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(f'SELECT user_id FROM users')
    data = cursor.fetchall()
    base.close()
    for d in data:
        data_list.append(d[0])
    return data_list


def clear_tasks(db_path: str, user_id: int):
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(
        f'DELETE FROM user_{user_id} WHERE is_ready = 0 AND is_canceled = 0')
    base.commit()
    base.close()
    clear_all(db_path, user_id)
    return


def clear_history(db_path: str, user_id: int):
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(
        f'DELETE FROM user_{user_id} WHERE is_ready = 1 OR is_canceled = 1')
    base.commit()
    base.close()
    clear_all(db_path, user_id)
    return


def clear_all(db_path: str, user_id: int, not_check=False):
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute('SELECT id FROM user_694624728')
    select = cursor.fetchall()
    if len(select) == 0 or not_check:
        cursor.execute(f'DROP TABLE user_{user_id}')
        cursor.execute(
            f'CREATE TABLE user_{user_id} (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL, is_ready BOOLEAN NOT NULL DEFAULT 0, is_canceled BOOLEAN NOT NULL DEFAULT 0, important BOOLEAN NOT NULL DEFAULT 1)')
    base.commit()
    base.close()
    return


def set_timezone(db_path: str, user_id: int, timezone: str):
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(
        f'UPDATE users SET timezone = {timezone} WHERE user_id = {user_id}')
    base.commit()
    base.close()


def add_time(db_path: str, user_id: int, time: str):
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(
        f'INSERT INTO time_{user_id} (time, status) VALUES ("{time}", 1) ON CONFLICT(time) DO UPDATE SET status=1')
    base.commit()
    base.close()


def add_task(db_path: str, user_id: int, text: str):
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(f'INSERT INTO user_{user_id} (text) VALUES ("{text}")')
    base.commit()
    base.close()


def mark_ready(db_path: str, user_id: int, id: int):
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(f'UPDATE user_{user_id} SET is_ready = 1 WHERE id = {id}')
    base.commit()
    base.close()


def mark_important(db_path: str, user_id: int, id: int):
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(f'UPDATE user_{user_id} SET important = 1 WHERE id = {id}')
    base.commit()
    base.close()


def mark_unimportant(db_path: str, user_id: int, id: int):
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(f'UPDATE user_{user_id} SET important = 0 WHERE id = {id}')
    base.commit()
    base.close()


def mark_canceled(db_path: str, user_id: int, id: int):
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(
        f'UPDATE user_{user_id} SET is_canceled = 1 WHERE id = {id}')
    base.commit()
    base.close()


def restore(db_path: str, user_id: int, id: int):
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(
        f'UPDATE user_{user_id} SET is_ready = 0, is_canceled = 0 WHERE id = {id}')
    base.commit()
    base.close()


def delete_task(db_path: str, user_id: int, id: int):
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(
        f'DELETE FROM user_{user_id} WHERE id = {id}')
    base.commit()
    base.close()
    clear_all(db_path, user_id)


def edit_task(db_path: str, user_id: int, id: int, text: str):
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(
        f'UPDATE user_{user_id} SET text = "{text}" WHERE id = {id}')
    base.commit()
    base.close()
    return


def turn_off_time(db_path: str, user_id: int, time: str):
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(
        f'UPDATE time_{user_id} SET status = 0 WHERE time = "{time}"')
    base.commit()


def turn_on_time(db_path: str, user_id: int, time: str):
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(
        f'UPDATE time_{user_id} SET status = 1 WHERE time = "{time}"')
    base.commit()


def delete_time(db_path: str, user_id: int, time: str):
    base = sqlite3.connect(db_path)
    cursor = base.cursor()
    cursor.execute(
        f'DELETE FROM time_{user_id} WHERE time = "{time}"')
    base.commit()
    base.close()
