import sqlite3
import hashlib

DB_NAME = "emotionsense.db"

def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_auth_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users VALUES (NULL, ?, ?)",
            (username, hash_pass(password))
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_pass(password))
    )

    user = cur.fetchone()
    conn.close()

    return user