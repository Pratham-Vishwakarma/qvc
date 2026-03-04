import hashlib
import json
from datetime import datetime
from .database import insert_commit, get_last_commit, get_staged_data

def commits(message):

    stage_data = get_staged_data()
    
    for i in stage_data:
        commit_data_str = {
            "circuit_json": json.loads(i[2]),
            "parameters": json.loads(i[3]),
            "statevector": json.loads(i[4]),
            "metadata": json.loads(i[5]),
            "message": message
        }

        parent = get_last_commit()
        commit_string = json.dumps(commit_data_str, sort_keys=True)
        commit_id = hashlib.sha256(commit_string.encode()).hexdigest()

        data = {
            "id": commit_id,
            "timestamp": datetime.now().astimezone().isoformat(),
            "parent_id": parent,
            "commit_data": commit_data_str
        }

        insert_commit(data)

        print("Committed:", commit_id)