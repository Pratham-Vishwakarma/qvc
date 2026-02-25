import uuid
from datetime import datetime
from .database import create_db, insert_commit, get_last_commit

def run(message):

    create_db()  # ensure repo exists

    commit_id = str(uuid.uuid4())
    parent = get_last_commit()

    data = {
        "id": commit_id,
        "timestamp": datetime.now().isoformat(),
        "message": message,
        "circuit_json": "placeholder",
        "parameters": "none",
        "statevector": "none",
        "metadata": "test",
        "parent_id": parent
    }

    insert_commit(data)

    print("Committed:", commit_id)