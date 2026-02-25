import QuantumCircuit from qiskit

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(1, 0)