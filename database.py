import sqlite3
import json
from datetime import datetime


def init_db():
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            summary TEXT,
            category TEXT,
            priority TEXT,
            priority_reason TEXT,
            actions TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_email(email, summary, category, priority, priority_reason, actions):
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO emails (email, summary, category, priority, priority_reason, actions, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (email, summary, category, priority, priority_reason, actions, timestamp))
    conn.commit()
    conn.close()


def get_history(limit: int = 20) -> list[dict]:
    conn = sqlite3.connect("emails.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, summary, category, priority, priority_reason, actions, timestamp
        FROM emails ORDER BY timestamp DESC LIMIT ?
    """, (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    for row in rows:
        try:
            row["actions"] = json.loads(row["actions"])
        except (json.JSONDecodeError, TypeError):
            row["actions"] = []
    return rows
