from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
import numpy as np

# Create parameters
theta1 = Parameter("θ1")
theta2 = Parameter("θ2")
theta3 = Parameter("θ3")

# 5-qubit circuit
qc = QuantumCircuit(5)

# -----------------------------------
# Layer 1 – Superposition
# -----------------------------------
for i in range(5):
    qc.h(i)

qc.barrier()

# -----------------------------------
# Layer 2 – Parametrized Rotations
# -----------------------------------
qc.rx(theta1, 0)
qc.ry(theta2, 1)
qc.rz(theta3, 2)
qc.rx(theta2, 3)
qc.ry(theta1, 4)

qc.barrier()

# -----------------------------------
# Layer 3 – Heavy Entanglement
# -----------------------------------
qc.cx(0, 1)
qc.cx(1, 2)
qc.cx(2, 3)
qc.cx(3, 4)

qc.cz(4, 0)

qc.barrier()

# -----------------------------------
# Layer 4 – Multi-Controlled Gate
# -----------------------------------
qc.mcx([0, 1, 2, 3], 4)

qc.barrier()

# -----------------------------------
# Layer 5 – QFT-style Controlled Phases
# -----------------------------------
qc.cp(np.pi/2, 0, 1)
qc.cp(np.pi/4, 0, 2)
qc.cp(np.pi/8, 0, 3)
qc.cp(np.pi/16, 0, 4)

qc.barrier()

# -----------------------------------
# Layer 6 – Randomized Rotations
# -----------------------------------
for i in range(5):
    qc.rx(np.random.rand(), i)
    qc.ry(np.random.rand(), i)
    qc.rz(np.random.rand(), i)

qc.barrier()

# -----------------------------------
# Final Entanglement Burst
# -----------------------------------
qc.swap(0, 4)
qc.swap(1, 3)

qc.ccx(0, 2, 4)

# Bind parameters to actual values
qc = qc.assign_parameters({
    theta1: np.pi / 3,
    theta2: np.pi / 5,
    theta3: np.pi / 7
})