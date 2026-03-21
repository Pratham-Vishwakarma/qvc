import sqlite3
import os
import json

DB_PATH = os.path.join(".qvc", "qvc.db")

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
        bindings TEXT,
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
        bindings TEXT,
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

    if not row or data["stage_id"] != row[0]:
        cur.execute("""
        INSERT INTO stage VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data["stage_id"],
            data["timestamp"],
            json.dumps(data["file_data"]["circuit_json"]),
            json.dumps(data["file_data"]["parameters"]),
            json.dumps(data["file_data"]["bindings"]),
            json.dumps(data["file_data"]["statevector"]),
            json.dumps(data["file_data"]["metadata"])
        ))

        conn.commit()
    conn.close()

def get_staged_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM stage ORDER BY timestamp DESC")
    row = cur.fetchall()

    conn.close()
    return row

def get_commited_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM commits ORDER BY timestamp DESC")
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
    INSERT INTO commits VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["id"],
        data["timestamp"],
        data["parent_id"],
        json.dumps(data["commit_data"]["circuit_json"]),
        json.dumps(data["commit_data"]["parameters"]),
        json.dumps(data["commit_data"]["bindings"]),
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

    conn.close()

    return row

def remove_from_stage(limit):
    conn = conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM stage ORDER BY timestamp DESC LIMIT 1")
    row = cur.fetchone()

    dels = []

    if row:
        cur.execute("DELETE FROM stage WHERE stage_id IN (SELECT stage_id FROM stage ORDER BY timestamp DESC LIMIT ?) RETURNING * ", (limit,))
        dels = cur.fetchall()
        
    conn.commit()
    conn.close()
    return row, dels

def restore_from_stage():
    conn = conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM commits ORDER BY timestamp DESC LIMIT 1")
    row = cur.fetchone()

    dels = []

    if row:
        cur.execute("DELETE FROM commits WHERE id IN (SELECT id FROM commits ORDER BY timestamp DESC LIMIT 1) RETURNING * ")
        dels = cur.fetchone()
        cur.execute("SELECT stage_id FROM stage ORDER BY timestamp DESC LIMIT 1")
        stg = cur.fetchone()
        if not stg or dels[0] != stg[0]:
            cur.execute("""
            INSERT INTO stage VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                dels[0],
                dels[1],
                dels[3],
                dels[4],
                dels[5],
                dels[6],
                dels[7]
            ))

    conn.commit()
    conn.close()
    return row, dels