import json
from .database import get_last_two_commits

def normalize(value):
    if value is None:
        return 0

    try:
        return float(value)
    except:
        return 0

def extract_params(data, binding):
    params = {}

    for i, gate in enumerate(data):
        name = gate["gate"]
        qubit = gate["qubits"]
        q_params = gate["params"]

        if not q_params:
            params[(i, name, tuple(qubit), "no_param")] = None

        for p in q_params:
            if isinstance(p, str):
                value = binding.get(p, 0)

                params[(i, name, tuple(qubit), p)] = value

            else:
                params[(i, name, tuple(qubit), f"theta{i+1}")] = p

    return params

def detailed_param_diff():

    file_a, file_b = get_last_two_commits()

    data_a = json.loads(file_a[3])
    binding_a = json.loads(file_a[5])
    data_b = json.loads(file_b[3])
    binding_b = json.loads(file_b[5])

    params_a = extract_params(data_a, binding_a)
    params_b = extract_params(data_b, binding_b)

    details = []

    all_keys = set(params_a.keys()) | set(params_b.keys())

    for key in sorted(all_keys):

        _, gate, qubit, param = key

        new = normalize(params_a.get(key))
        old = normalize(params_b.get(key))

        if old == new:
            details.append(f"""
Gate: {gate} (qubit {qubit})
{param}
 Unchanged ({old:.2f})
""")

        else:
            delta = new - old
            drift = abs(delta)

            if drift < 0.1:
                impact = "Low"
            elif drift < 0.5:
                impact = "Moderate"
            else:
                impact = "High"

            sign = "+" if delta > 0 else ""

            details.append(f"""
Gate: {gate} (qubit {qubit})
{param}
 Old: {old:.2f}
 New: {new:.2f}
 Delta: {sign}{delta:.2f}
 Impact: {impact}
""")

    return "".join(details)

def summary_param_diff():

    file_a, file_b = get_last_two_commits()

    data_a = json.loads(file_a[3])
    binding_a = json.loads(file_a[5])
    data_b = json.loads(file_b[3])
    binding_b = json.loads(file_b[5])

    params_a = extract_params(data_a, binding_a)
    params_b = extract_params(data_b, binding_b)

    all_keys = set(params_a.keys()) | set(params_b.keys())
    changed = 0
    unchanged = 0
    total_drift = 0
    max_drift = 0
    added = 0
    removed = 0

    for key in sorted(all_keys):

        new = normalize(params_a.get(key))
        old = normalize(params_b.get(key))

        if old == new:
            unchanged += 1

        else:
            if key not in params_a:
                added += 1
            
            if key not in params_b:
                removed += 1

            changed += 1

            delta = new - old
            drift = abs(delta)

            total_drift += drift
            max_drift = max(max_drift, drift)

    if max_drift <= 0.1:
        overall = "Low"
    elif max_drift <= 0.5:
        overall = "Moderate"
    else:
        overall = "High"

    summary = f"""
Total Parameters: {len(all_keys)}
Changed Parameters: {changed}
Added Parameters: {added}
Removed Parameters: {removed}
Unchanged: {unchanged}
Total Drift: {total_drift:.2f}
Max Drift: {max_drift:.2f}
Overall Impact: {overall}
"""

    return summary.strip()
    
params_a = {
    ("rx", 0, "theta"): 0.5,
    ("u", 1, "gamma"): 0.3,
    ("rx", 0, "alpha"): 0.5,
}

params_b = {
    ("rx", 0, "theta"): 0.8,
    ("u", 1, "gamma"): 0.3
}

# print(summary_param_diff())
# print(detailed_param_diff())