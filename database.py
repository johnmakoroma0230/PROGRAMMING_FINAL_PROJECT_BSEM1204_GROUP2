import sqlite3

DB_NAME = "hilltop_records.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def setup_database():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        gender TEXT NOT NULL,
        phone TEXT,
        address TEXT,
        status TEXT NOT NULL,
        created_date TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()