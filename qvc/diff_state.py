import json
import numpy as np
from .database import get_last_two_commits

def convert_statevector(json_state):

    complex_state = []

    for amp in json_state:
        complex_number = complex(amp["real"], amp["imag"])
        complex_state.append(complex_number)

    return complex_state

def compute_fidelity(state1, state2):

    psi1 = np.array(state1, dtype=complex)
    psi2 = np.array(state2, dtype=complex)

    inner_product = np.vdot(psi1, psi2)

    fidelity = abs(inner_product) ** 2

    return fidelity

def state_distance(state1, state2):

    psi1 = np.array(state1, dtype=complex)
    psi2 = np.array(state2, dtype=complex)

    return np.linalg.norm(psi1 - psi2)

def classify_impact(fidelity):

    if fidelity > 0.999:
        return "Identical"

    elif fidelity > 0.95:
        return "Minimal Change"

    elif fidelity > 0.80:
        return "Moderate Change"

    else:
        return "Major Change"

def amplitude_changes(state1, state2, threshold=0.01):

    changes = []

    n_qubits = int(np.log2(len(state1)))

    for i in range(len(state1)):

        old = state1[i]
        new = state2[i]

        delta = abs(new - old)

        if delta > threshold:

            basis = format(i, f"0{n_qubits}b")

            changes.append({
                "basis": f"|{basis}>",
                "old": old,
                "new": new,
                "delta": delta
            })

    return changes

def summary_state_diff():
    file_a, file_b = get_last_two_commits()

    state1 = convert_statevector(json.loads(file_a[6]))
    state2 = convert_statevector(json.loads(file_b[6]))

    if len(state1) != len(state2):
        raise ValueError("Statevectors must have same dimension")

    fidelity = compute_fidelity(state1, state2)

    distance = state_distance(state1, state2)

    impact = classify_impact(fidelity)

    changes = amplitude_changes(state1, state2)

    summary = f"""
Fidelity: {fidelity:.4f}
Distance: {distance:.4f}
Impact: {impact}
Number of Amplitude Changes: {len(changes)}
"""

    return summary.strip()

def detailed_state_diff():
    details = []

    file_a, file_b = get_last_two_commits()

    state1 = convert_statevector(json.loads(file_a[6]))
    state2 = convert_statevector(json.loads(file_b[6]))

    if len(state1) != len(state2):
        raise ValueError("Statevectors must have same dimension")

    fidelity = compute_fidelity(state1, state2)

    distance = state_distance(state1, state2)

    impact = classify_impact(fidelity)

    changes = amplitude_changes(state1, state2)

    details.append(f"""
Exact Fidelity: {fidelity}
Exact Distance: {distance}
Impact: {impact}
Amplitude Changes:
""")

    if not changes:
        details.append(f"""
No significant amplitude changes
""")

    for c in changes:
        details.append(f"""
{c['basis']} : {c['old']} → {c['new']} (Δ {c['delta']:.4f})""")

    return "\n".join(details)