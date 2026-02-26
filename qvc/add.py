import os, sys
import json
import hashlib
import importlib.util
from datetime import datetime, UTC
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def extract_snapshot(circuit: QuantumCircuit):

    # 1. Convert gate list
    gate_list = []

    for operation, qubits, clbits in circuit.data:
        gate_info = {
            "gate": operation.name,
            "qubits": [circuit.find_bit(q).index for q in qubits],
            "clbits": [circuit.find_bit(c).index for c in clbits] if clbits else [],
            "params": [
                float(p) if hasattr(p, "__float__") else str(p)
                for p in operation.params
            ],
        }
        gate_list.append(gate_info)

    # 2. Extract parameters
    parameters = {}

    for param in circuit.parameters:
        parameters[str(param)] = None

    # 3. Get statevector
    try:
        statevector = Statevector.from_instruction(circuit)
        statevector_list = [
            {
                "real": float(amplitude.real),
                "imag": float(amplitude.imag),
            }
            for amplitude in statevector.data
        ]
    except Exception as e:
        statevector_list = str(e)

    # 4. Metadata
    metadata = {
        "num_qubits": circuit.num_qubits,
        "num_clbits": circuit.num_clbits,
        "depth": circuit.depth(),
        "size": circuit.size(),
        "global_phase": float(circuit.global_phase)
    }

    # Integration of above components
    snapshot = {
        "circuit_json": gate_list,
        "parameters": parameters,
        "statevector": statevector_list,
        "metadata": metadata,
        "timestamp": datetime.now().astimezone().isoformat()
    }

    return snapshot

# -------------------------------------------------
# Snapshot Storage
# -------------------------------------------------

def store_snapshot(snapshot: dict):

    snapshot_str = json.dumps(snapshot, sort_keys=True)
    snapshot_hash = hashlib.sha256(snapshot_str.encode()).hexdigest()
    os.makedirs(".qvc/logs", exist_ok=True)
    file_path = f".qvc/logs/{snapshot_hash}.json"
    with open(file_path, "w") as f:
        json.dump(snapshot, f, indent=4)

    return snapshot_hash, file_path

def load_circuit_from_file(filepath):

    spec = importlib.util.spec_from_file_location("circuit_module", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, QuantumCircuit):
            return attr

    raise ValueError("No QuantumCircuit object found in file.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python qvc\\add.py <file.py>")
        sys.exit(1)

    target = sys.argv[1]

    if target == ".":
        target = "Test_code2.py"  # default file name

    qc = load_circuit_from_file(target)

    snapshot = extract_snapshot(qc)
    snapshot_id, path = store_snapshot(snapshot)

    print("Snapshot stored successfully!")
    print("Snapshot ID:", snapshot_id)
    print("Location:", path)