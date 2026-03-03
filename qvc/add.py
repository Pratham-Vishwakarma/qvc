import os, sys
import json
import hashlib
import importlib.util
from datetime import datetime, UTC
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from .database import insert_stage

# Generate the compiled data of gates.
def generate(circuit: QuantumCircuit):

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
    metadata = [{
        "num_qubits": circuit.num_qubits,
        "num_clbits": circuit.num_clbits,
        "depth": circuit.depth(),
        "size": circuit.size(),
        "global_phase": float(circuit.global_phase)
    }]

    # Integration of above components
    file_data = {
        "circuit_json": gate_list,
        "parameters": parameters,
        "statevector": statevector_list,
        "metadata": metadata
    }

    return file_data

# Add the data to the staging area.
def stage(file_data: dict):

    file_data_str = json.dumps(file_data, sort_keys=True)
    stage_hash = hashlib.sha256(file_data_str.encode()).hexdigest()
    insert_stage({
        "id": stage_hash,
        "timestamp": datetime.now().astimezone().isoformat(),
        "file_data": file_data
    })

    return

# Load the ciruit from the given file.
def load_circuit_from_file(filepath):

    spec = importlib.util.spec_from_file_location("circuit_module", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, QuantumCircuit):
            return attr

    raise ValueError("No QuantumCircuit object found in file.")