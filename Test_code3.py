from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

# Global parameters (shared across gates)
theta = Parameter('theta')
alpha = Parameter('alpha')

# Local parameters
beta = Parameter('beta')
gamma = Parameter('gamma')
delta = Parameter('delta')

# Create circuit
qc = QuantumCircuit(2)

# Basic gate
qc.h(0)

# Gates using parameters
qc.rx(theta, 0)        # global parameter
qc.ry(alpha, 1)        # global parameter

qc.rz(beta, 0)         # local parameter
qc.u(gamma, 0.5, 0.2, 1)  # local parameter

# Controlled gate using global parameter
qc.crx(delta, 0, 1)

qc = qc.assign_parameters({
    theta: 0.7,
    alpha: 1.2,
    delta: 1.5
})
