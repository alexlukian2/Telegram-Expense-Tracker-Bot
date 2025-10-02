import sqlite3
import os
from datetime import datetime

DB_NAME = os.getenv("DB_PATH", "/var/tmp/finance.db")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            category TEXT,
            type TEXT, -- 'income' або 'expense'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_record(user_id, amount, category, record_type):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO records (user_id, amount, category, type)
        VALUES (?, ?, ?, ?)
    """, (user_id, amount, category, record_type))
    conn.commit()
    conn.close()

def get_stats(user_id, period="month"):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if period == "week":
        cur.execute("""
            SELECT category, SUM(amount) 
            FROM records 
            WHERE user_id = ? 
              AND created_at >= datetime('now', '-7 day') 
              AND type = 'expense'
            GROUP BY category
        """, (user_id,))
    elif period == "month":
        cur.execute("""
            SELECT category, SUM(amount) 
            FROM records 
            WHERE user_id = ? 
              AND strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
              AND type = 'expense'
            GROUP BY category
        """, (user_id,))
    else:  # all time
        cur.execute("""
            SELECT category, SUM(amount) 
            FROM records 
            WHERE user_id = ? 
              AND type = 'expense'
            GROUP BY category
        """, (user_id,))

    expenses = cur.fetchall()

    cur.execute("""
        SELECT SUM(amount) FROM records 
        WHERE user_id = ? AND type = 'income'
    """, (user_id,))
    income = cur.fetchone()[0] or 0

    cur.execute("""
        SELECT SUM(amount) FROM records 
        WHERE user_id = ? AND type = 'expense'
    """, (user_id,))
    expense = cur.fetchone()[0] or 0

    conn.close()
    return expenses, income, expense
