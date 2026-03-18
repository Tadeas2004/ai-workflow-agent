import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            shrnuti TEXT,
            kategorie TEXT,
            priorita TEXT,
            akce TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_email(email, shrnuti, kategorie, priorita, akce):
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO emails (email, shrnuti, kategorie, priorita, akce, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (email, shrnuti, kategorie, priorita, akce, timestamp))

    conn.commit()
    conn.close()