import os, sys
import copy
import json
import hashlib
import importlib.util
from datetime import datetime, UTC
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from .database import insert_stage, get_staged_data

# Generate the compiled data of gates.
def generate(circuit: QuantumCircuit):

    # 1. Convert gate list
    gate_list = []

    for operation, qubits, clbits in circuit.data:
        
        params = []

        for p in operation.params:
            try:
                params.append(float(p))
            except TypeError:
                params.append(str(p))

        gate_info = {
            "gate": operation.name,
            "qubits": [circuit.find_bit(q).index for q in qubits],
            "clbits": [circuit.find_bit(c).index for c in clbits] if clbits else [],
            "params": params
        }
        gate_list.append(gate_info)

    # 2. Extract parameters
    parameters = {}

    for param in circuit.parameters:
        parameters[str(param)] = {
            "name": param.name,
            "uuid": str(param.uuid)
        }

    # 3. Extract bindings (bound values + 0 for unbound)
    bindings = {}

    for operation, _, _ in circuit.data:
        for p in operation.params:

            # ignore pure numeric constants
            try:
                float(p)
                continue
            except TypeError:
                name = str(p)
                if name not in bindings:
                    bindings[name] = 0

    # 4. Metadata
    metadata = [{
        "num_qubits": circuit.num_qubits,
        "num_clbits": circuit.num_clbits,
        "depth": circuit.depth(),
        "size": circuit.size(),
        "global_phase": float(circuit.global_phase)
    }]

    # 5. Get statevector
    sim_circuit = circuit.copy()

    if sim_circuit.parameters:
        zero_bindings = {param: 0 for param in sim_circuit.parameters}
        sim_circuit = sim_circuit.assign_parameters(zero_bindings)

    try:
        statevector = Statevector.from_instruction(sim_circuit)
        statevector_list = [
            {
                "real": float(amplitude.real),
                "imag": float(amplitude.imag),
            }
            for amplitude in statevector.data
        ]
    except Exception as e:
        statevector_list = str(e)

    # Integration of above components
    file_data = {
        "circuit_json": gate_list,
        "parameters": parameters,
        "bindings": bindings,
        "statevector": statevector_list,
        "metadata": metadata
    }

    return file_data

def prepare_hash_data(file_data):
    data = copy.deepcopy(file_data)

    # remove UUIDs from parameters
    for p in data["parameters"].values():
        if "uuid" in p:
            del p["uuid"]

    return data

# Add the data to the staging area.
def stage(file_data: dict):
    hash_file_data = prepare_hash_data(file_data)

    file_data_str = json.dumps(hash_file_data, sort_keys=True)
    stage_hash = hashlib.sha256(file_data_str.encode()).hexdigest()
    
    stage_data = get_staged_data()

    for i in range(len(stage_data)):
        if stage_data is not None and stage_data[i][0] == stage_hash:
            print("Cannot stage the file, Found data same as previously staged.")
            return

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