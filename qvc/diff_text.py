import json
import difflib

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def stringify_gates(gates):
    """
    Convert gate JSON objects into stable strings
    so difflib can compare them.
    """
    return [json.dumps(g, sort_keys=True) for g in gates]


def detailed_diff(file_a, file_b):

    data_a = load_json(file_a)
    data_b = load_json(file_b)

    # gates_a = stringify_gates(data_a.get("gates", []))
    # gates_b = stringify_gates(data_b.get("gates", []))

    gates_a = stringify_gates([item["gate"] for item in data_a])
    gates_b = stringify_gates([item["gate"] for item in data_b])

    diff = difflib.unified_diff(
        gates_a,
        gates_b,
        fromfile="Commit A",
        tofile="Commit B",
        lineterm=""
    )

    return "\n".join(diff)


def summary_diff(file_a, file_b):

    data_a = load_json(file_a)
    data_b = load_json(file_b)

    # gates_a = stringify_gates(data_a.get("gates", []))
    # gates_b = stringify_gates(data_b.get("gates", []))

    gates_a = stringify_gates([item["gate"] for item in data_a])
    gates_b = stringify_gates([item["gate"] for item in data_b])

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

    # depth_a = data_a.get("depth", 0)
    # depth_b = data_b.get("depth", 0)

    depth_a = max([item["depth"] for item in data_a])
    depth_b = max([item["depth"] for item in data_b])

    summary = f"""
============================
TEXT DIFF SUMMARY
============================
Gates Added: {added}
Gates Removed: {removed}
Gates Modified: {modified}
Total Gate Count: {len(gates_a)} → {len(gates_b)}
Circuit Depth: {depth_a} → {depth_b}
"""

    return summary.strip()