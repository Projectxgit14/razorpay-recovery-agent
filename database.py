import sqlite3
from datetime import datetime

DB_NAME = "audit_trail.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recovery_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL,
            original_amount REAL NOT NULL,
            failure_reason TEXT NOT NULL,
            ai_reasoning TEXT,
            approved_discount_pct REAL,
            final_amount REAL,
            payment_link TEXT,
            status TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_audit(order_id, original_amount, failure_reason, ai_reasoning, discount_pct, final_amount, payment_link, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO recovery_audit 
        (order_id, original_amount, failure_reason, ai_reasoning, approved_discount_pct, final_amount, payment_link, status, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (order_id, original_amount, failure_reason, ai_reasoning, discount_pct, final_amount, payment_link, status, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")