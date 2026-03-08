import json
import difflib
from .database import get_last_two_commits

def load_data(data, metadata):
    result = []

    if metadata:
        md = metadata[0]
        if md.get("num_qubits") is not None:
            nq=f"num_qb:{md['num_qubits']}"
        if md.get("num_clbits") is not None:
            nc=f"num_cb:{md['num_clbits']}"    
        if md.get("depth") is not None:
            d=f"d:{md['depth']}"
        if md.get("size") is not None:
            s=f"s:{md['size']}"
        if md.get("global_phase") is not None:
            gbl_phs=f"gbl_phs:{md['global_phase']}"
        if md:
            result.append(f"{nq} {nc} {d} {s} {gbl_phs}")
        result.append("")
    
    for g in data:
        gate = g["gate"]
        qubits = ", ".join(f"q[{q}]" for q in g["qubits"])
        params = ", ".join(map(str, g["params"]))

        if params:
            result.append(f"{gate}({params}) {qubits}")
        else:
            result.append(f"{gate} {qubits}")

    return result

def detailed_diff():

    file_a, file_b = get_last_two_commits()

    data_a = json.loads(file_a[3])
    metadata_a = json.loads(file_a[6])
    data_b = json.loads(file_b[3])
    metadata_b = json.loads(file_b[6])
    
    gates_a = load_data(data_a, metadata_a)
    gates_b = load_data(data_b, metadata_b)

    diff = difflib.unified_diff(
        gates_a,
        gates_b,
        fromfile="Commit A",
        tofile="Commit B",
        lineterm=""
    )

    return "\n".join(diff)

def summary_diff():

    file_a, file_b = get_last_two_commits()

    data_a = json.loads(file_a[3])
    metadata_a = json.loads(file_a[6])
    data_b = json.loads(file_b[3])
    metadata_b = json.loads(file_b[6])

    gates_a = [item["gate"] for item in data_a]
    gates_b = [item["gate"] for item in data_b]

    added = 0
    removed = 0
    modified = 0

    matcher = difflib.SequenceMatcher(None, gates_a, gates_b)

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():

        if tag == "insert":
            added += (j2 - j1)

        elif tag == "delete":
            removed += (i2 - i1)

        elif tag == "replace":
            modified += min(i2 - i1, j2 - j1)

            if (j2 - j1) > (i2 - i1):
                added += (j2 - j1) - (i2 - i1)

            elif (i2 - i1) > (j2 - j1):
                removed += (i2 - i1) - (j2 - j1)

    depth_a = metadata_a[0]["depth"] if metadata_a else "N/A"
    depth_b = metadata_b[0]["depth"] if metadata_b else "N/A"

    summary = f"""
Total Gate Count: {len(gates_a)} → {len(gates_b)}
Gates Added: {added}
Gates Removed: {removed}
Gates Modified: {modified}
Circuit Depth: {depth_a} → {depth_b}
"""

    return summary.strip()