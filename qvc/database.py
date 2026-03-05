import sqlite3
import os
import json

DB_PATH = os.path.join(".qvc", "commits.db")

def create_db():
    os.makedirs(".qvc", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS commits (
        id TEXT PRIMARY KEY,
        timestamp TEXT,
        parent_id TEXT,
        circuit_json TEXT,
        parameters TEXT,
        statevector TEXT,
        metadata TEXT,
        message TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS stage (
        stage_id TEXT PRIMARY KEY,
        timestamp TEXT,
        circuit_json TEXT,
        parameters TEXT,
        statevector TEXT,
        metadata TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_stage(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT stage_id FROM stage ORDER BY timestamp DESC LIMIT 1")
    row = cur.fetchone()

    if not row or data["id"] != row[0]:
        cur.execute("""
        INSERT INTO stage VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["id"],
            data["timestamp"],
            json.dumps(data["file_data"]["circuit_json"]),
            json.dumps(data["file_data"]["parameters"]),
            json.dumps(data["file_data"]["statevector"]),
            json.dumps(data["file_data"]["metadata"])
        ))

        conn.commit()
    conn.close()

def get_staged_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM stage")
    row = cur.fetchall()

    conn.close()
    return row

def get_last_commit():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT id FROM commits ORDER BY timestamp DESC LIMIT 1")
    row = cur.fetchone()

    conn.close()
    return row[0] if row else None

def insert_commit(data):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO commits VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["id"],
        data["timestamp"],
        data["parent_id"],
        json.dumps(data["commit_data"]["circuit_json"]),
        json.dumps(data["commit_data"]["parameters"]),
        json.dumps(data["commit_data"]["statevector"]),
        json.dumps(data["commit_data"]["metadata"]),
        json.dumps(data["commit_data"]["message"])
    ))

    conn.commit()
    conn.close()

def clear_stage():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DELETE FROM stage")

    conn.commit()
    conn.close()

def get_last_two_commits():
    conn = conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM COMMITS ORDER BY timestamp DESC LIMIT 2")
    row = cur.fetchall()

    cur.close()

    return row