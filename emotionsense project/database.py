import sqlite3

DB_NAME = "emotionsense.db"

def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        text TEXT,
        emotion TEXT,
        confidence REAL
    )
    """)

    conn.commit()
    conn.close()

def save_review(username, text, emotion, confidence):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reviews (username, text, emotion, confidence)
        VALUES (?, ?, ?, ?)
    """, (username, text, emotion, confidence))

    conn.commit()
    conn.close()

def get_reviews(username):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT text, emotion, confidence
        FROM reviews
        WHERE username = ?
    """, (username,))

    data = cur.fetchall()

    conn.close()
    return data

def clear_reviews(username):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM reviews
        WHERE username = ?
    """, (username,))

    conn.commit()
    conn.close()