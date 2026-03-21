import hashlib
import json
import copy
from datetime import datetime
from .database import insert_commit, get_last_commit, get_staged_data, clear_stage

def prepare_hash_data(file_data):
    data = {
        "circuit_json": file_data["circuit_json"],
        "parameters": {
            k: {"name": v["name"]}
            for k, v in file_data["parameters"].items()
        },
        "bindings": file_data["bindings"],
        "statevector": file_data["statevector"],
        "metadata": file_data["metadata"],
        "message": file_data["message"]
    }
    return data

def commits(message):
    stage_data = get_staged_data()
    
    for i in stage_data:
        commit_data_str = {
            "circuit_json": json.loads(i[2]),
            "parameters": json.loads(i[3]),
            "bindings": json.loads(i[4]),
            "statevector": json.loads(i[5]),
            "metadata": json.loads(i[6]),
            "message": message
        }

        parent = get_last_commit()
        hash_commit_data = prepare_hash_data(commit_data_str)
        commit_string = json.dumps(hash_commit_data, sort_keys=True)
        commit_id = hashlib.sha256(commit_string.encode()).hexdigest()

        data = {
            "id": commit_id,
            "timestamp": datetime.now().astimezone().isoformat(),
            "parent_id": parent,
            "commit_data": commit_data_str
        }

        insert_commit(data)

        print("Committed:", commit_id)
    
    clear_stage()