import sqlite3
import os

DB_PATH = os.path.join(".qvc", "commits.db")


def create_db():
    os.makedirs(".qvc", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS commits (
        id TEXT PRIMARY KEY,
        timestamp TEXT,
        message TEXT,
        circuit_json TEXT,
        parameters TEXT,
        statevector TEXT,
        metadata TEXT,
        parent_id TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_commit(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO commits VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["id"],
        data["timestamp"],
        data["message"],
        data["circuit_json"],
        data["parameters"],
        data["statevector"],
        data["metadata"],
        data["parent_id"]
    ))

    conn.commit()
    conn.close()


def get_last_commit():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT id FROM commits ORDER BY timestamp DESC LIMIT 1")
    row = cur.fetchone()

    conn.close()
    return row[0] if row else None