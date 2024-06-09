import sqlite3
from flask import current_app

def init_db():
    with sqlite3.connect(current_app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                name TEXT,
                dob TEXT,
                job TEXT,
                mental_health_status TEXT DEFAULT 'neutral',
                hobby TEXT,
                physical_health TEXT,
                others TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                role_info TEXT,
                history_info TEXT,
                intention TEXT,
                target TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        conn.commit()

def get_user_id(username):
    with sqlite3.connect(current_app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            return user[0]
        cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
        conn.commit()
        return cursor.lastrowid

def get_user_info(user_id):
    with sqlite3.connect(current_app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name, dob, job, mental_health_status, hobby, physical_health, others FROM users WHERE id = ?', (user_id,))
        return cursor.fetchone()

def update_user_info(user_id, name=None, dob=None, job=None, mental_health_status=None, hobby=None, physical_health=None, others=None):
    with sqlite3.connect(current_app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET name = COALESCE(?, name),
                dob = COALESCE(?, dob),
                job = COALESCE(?, job),
                mental_health_status = COALESCE(?, mental_health_status),
                hobby = COALESCE(?, hobby),
                physical_health = COALESCE(?, physical_health),
                others = COALESCE(?, others)
            WHERE id = ?
        ''', (name, dob, job, mental_health_status, hobby, physical_health, others, user_id))
        conn.commit()

def get_conversation_history(user_id):
    with sqlite3.connect(current_app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT role_info, history_info, intention, target FROM conversations WHERE user_id = ?', (user_id,))
        conversation = cursor.fetchone()
        if conversation:
            return conversation[0], conversation[1], conversation[2], conversation[3]
        return "", "", "", ""

def update_conversation_history(user_id, role_info, history_info, intention, target):
    with sqlite3.connect(current_app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('REPLACE INTO conversations (user_id, role_info, history_info, intention, target) VALUES (?, ?, ?, ?, ?)',
                       (user_id, role_info, history_info, intention, target))
        conn.commit()
