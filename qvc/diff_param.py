def normalize(value):
    if value is None:
        return 0
    return value

def parameter_diff(params_a, params_b):

    total_params = max(len(params_a), len(params_b))
    changed = 0
    unchanged = 0
    total_drift = 0
    max_drift = 0
    details = []

    for i in range(total_params):

        old = normalize(params_a[i] if i < len(params_a) else 0)
        new = normalize(params_b[i] if i < len(params_b) else 0)

        if old == new:
            unchanged += 1
            details.append(f"""
Param[{i}]:
 Unchanged ({old})
""")

        else:
            changed += 1
            delta = new - old
            drift = abs(delta)

            total_drift += drift
            max_drift = max(max_drift, drift)

            if drift < 0.1:
                impact = "Low"
            elif drift < 0.5:
                impact = "Moderate"
            else:
                impact = "High"

            sign = "+" if delta > 0 else ""

            details.append(f"""
Param[{i}]:
 Old: {old}
 New: {new}
 Delta: {sign}{delta}
 Impact: {impact}
""")

    return "".join(details)

def summary_param_diff(params_a, params_b):

    total_params = max(len(params_a), len(params_b))
    changed = 0
    unchanged = 0
    total_drift = 0
    max_drift = 0

    for i in range(total_params):

        old = normalize(params_a[i] if i < len(params_a) else 0)
        new = normalize(params_b[i] if i < len(params_b) else 0)

        if old == new:
            unchanged += 1

        else:
            changed += 1
            delta = new - old
            drift = abs(delta)

            total_drift += drift
            max_drift = max(max_drift, drift)

    if max_drift < 0.1:
        overall = "Low"
    elif max_drift < 0.5:
        overall = "Moderate"
    else:
        overall = "High"

    summary = f"""
Total Parameters: {total_params}
Changed Parameters: {changed}
Unchanged: {unchanged}
Total Drift: {total_drift:.2f}
Max Drift: {max_drift:.2f}
Overall Impact: {overall}
"""

    return summary.strip()
    
params_a = [0.5, None, -0.3]
params_b = [0.8, 1.2, None]

# print(summary_param_diff(params_a, params_b))