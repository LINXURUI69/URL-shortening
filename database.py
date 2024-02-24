import sqlite3


def clear_user_table():
    conn = sqlite3.connect('/app/users.db')
    c = conn.cursor()
    c.execute('''
        DELETE FROM users
    ''')
    conn.commit()
    conn.close()
def create_user_table():
    conn = sqlite3.connect('/app/users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
            )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect('/app/users.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (username, password) VALUES (?, ?)
    ''', (username, password))
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect('/app/users.db')
    c = conn.cursor()
    c.execute('''
        SELECT password FROM users WHERE username = ?
    ''', (username,))
    stored_password = c.fetchone()
    conn.close()
    if stored_password and stored_password[0] == password:
        return True
    return False

def update_password(username, new_password):
    conn = sqlite3.connect('/app/users.db')
    c = conn.cursor()
    c.execute('''
        UPDATE users SET password = ? WHERE username = ?
    ''', (new_password, username))
    conn.commit()
    conn.close()

def is_existing_user(username):
    conn = sqlite3.connect('/app/users.db')
    c = conn.cursor()
    c.execute('''
        SELECT username FROM users WHERE username = ?
    ''', (username,))
    is_exist = c.fetchone() is not None
    conn.close()
    return is_exist

def get_password(username):
    conn = sqlite3.connect('/app/users.db')
    c = conn.cursor()
    c.execute('''
        SELECT password FROM users WHERE username = ?
    ''', (username,))
    password = c.fetchone()[0]
    conn.close()
    return password