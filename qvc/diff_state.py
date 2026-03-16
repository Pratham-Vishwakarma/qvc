import numpy as np


# ---------------------------------
# Convert JSON statevector → complex
# ---------------------------------
def convert_statevector(json_state):

    complex_state = []

    for amp in json_state:
        complex_number = complex(amp["real"], amp["imag"])
        complex_state.append(complex_number)

    return complex_state


# ---------------------------------
# Fidelity
# ---------------------------------
def compute_fidelity(state1, state2):

    psi1 = np.array(state1, dtype=complex)
    psi2 = np.array(state2, dtype=complex)

    inner_product = np.vdot(psi1, psi2)

    fidelity = abs(inner_product) ** 2

    return fidelity


# ---------------------------------
# Distance
# ---------------------------------
def state_distance(state1, state2):

    psi1 = np.array(state1, dtype=complex)
    psi2 = np.array(state2, dtype=complex)

    return np.linalg.norm(psi1 - psi2)


# ---------------------------------
# Impact classification
# ---------------------------------
def classify_impact(fidelity):

    if fidelity > 0.999:
        return "Identical"

    elif fidelity > 0.95:
        return "Minimal Change"

    elif fidelity > 0.80:
        return "Moderate Change"

    else:
        return "Major Change"


# ---------------------------------
# Detect amplitude changes
# ---------------------------------
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


# ---------------------------------
# Summary output
# ---------------------------------
def print_summary(fidelity, distance, impact, changes):

    print("\nSTATE DIFF SUMMARY")
    print("---------------------")

    print(f"Fidelity: {fidelity:.4f}")
    print(f"Distance: {distance:.4f}")
    print(f"Impact: {impact}")
    print(f"Amplitude Changes: {len(changes)}")


# ---------------------------------
# Detailed output
# ---------------------------------
def print_details(fidelity, distance, changes):

    print("\nSTATE DIFF DETAILS")
    print("---------------------")

    print(f"Exact Fidelity: {fidelity}")
    print(f"Exact Distance: {distance}")

    print("\nAmplitude Changes:")

    if not changes:
        print("No significant amplitude changes")

    for c in changes:
        print(
            f"{c['basis']} : {c['old']} → {c['new']} (Δ {c['delta']:.4f})"
        )


# ---------------------------------
# Main state diff function
# ---------------------------------
def state_diff(json_state1, json_state2):

    state1 = convert_statevector(json_state1)
    state2 = convert_statevector(json_state2)

    if len(state1) != len(state2):
        raise ValueError("Statevectors must have same dimension")

    fidelity = compute_fidelity(state1, state2)

    distance = state_distance(state1, state2)

    impact = classify_impact(fidelity)

    changes = amplitude_changes(state1, state2)

    print_summary(fidelity, distance, impact, changes)

    print_details(fidelity, distance, changes)


# ---------------------------------
# Example test
# ---------------------------------
if __name__ == "__main__":

    stateA = [
        {"real": 0.548218300414465, "imag": -0.20011530103878566},
        {"real": 0.5625214131757257, "imag": -0.2539159377017891},
        {"real": 0.3750563183200591, "imag": 0.13690624335301174},
        {"real": 0.34093998328541997, "imag": 0.0534442148145433}
    ]

    stateB = [
        {"real": 0.5418218300414465, "imag": -0.50011530103878566},
        {"real": 0.6625214131758257, "imag": -0.8539159377017891},
        {"real": 0.9750563183200561, "imag": 0.13690624935301174},
        {"real": 0.34093998328541995, "imag": 0.7534442148145433}
    ]

    state_diff(stateA, stateB)