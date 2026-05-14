import sqlite3
import json
from datetime import datetime


def init_db():
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gmail_id TEXT UNIQUE,  -- added UNIQUE constraint to prevent duplicates
            email TEXT,
            summary TEXT,
            category TEXT,
            priority TEXT,
            priority_reason TEXT,
            actions TEXT,
            confidence REAL,
            sentiment TEXT,
            actionability TEXT,
            requires_response INTEGER,
            follow_up_needed INTEGER,
            deadline TEXT,
            entities TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def is_email_processed(gmail_id: str) -> bool:
    """Checks if this email has already been analyzed."""
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM emails WHERE gmail_id = ?", (gmail_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def save_email(gmail_id: str, email: str, result: dict):
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    priority = result.get("priority", {})
    
    # Using INSERT OR IGNORE just in case
    cursor.execute("""
        INSERT OR IGNORE INTO emails (
            gmail_id, email, summary, category, priority, priority_reason,
            actions, confidence, sentiment, actionability,
            requires_response, follow_up_needed, deadline, entities, timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        gmail_id,
        email,
        result.get("summary", ""),
        result.get("category", ""),
        priority.get("level", ""),
        priority.get("reason", ""),
        json.dumps(result.get("action_items", [])),
        result.get("confidence", 0.0),
        result.get("sentiment", ""),
        result.get("actionability", ""),
        1 if result.get("requires_response") else 0,
        1 if result.get("follow_up_needed") else 0,
        result.get("deadline"),
        json.dumps(result.get("entities", {})),
        timestamp
    ))
    conn.commit()
    conn.close()


def get_history(limit: int = 20) -> list[dict]:
    conn = sqlite3.connect("emails.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM emails ORDER BY timestamp DESC LIMIT ?
    """, (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    for row in rows:
        try:
            row["actions"] = json.loads(row["actions"])
        except (json.JSONDecodeError, TypeError):
            row["actions"] = []
        try:
            row["entities"] = json.loads(row["entities"])
        except (json.JSONDecodeError, TypeError):
            row["entities"] = {}
        row["requires_response"] = bool(row.get("requires_response"))
        row["follow_up_needed"] = bool(row.get("follow_up_needed"))
    return rows

def get_latest_email_record() -> dict | None:
    """Vrátí úplně poslední přidaný záznam z databáze jako klasický slovník, nebo None."""
    conn = sqlite3.connect("emails.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emails ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    
    if row:
        record = dict(row)
        
        try:
            record["actions"] = json.loads(record["actions"])
        except (json.JSONDecodeError, TypeError):
            record["actions"] = []
            
        try:
            record["entities"] = json.loads(record["entities"])
        except (json.JSONDecodeError, TypeError):
            record["entities"] = {}
            
        return record
        
    return None
