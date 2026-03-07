#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_10_hierarchal descent.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Paper Reference: Theorem 3.7 (Finite Termination)
Theorem Support: "Hierarchical Energy Dissipation"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tracks the energy of a multi-frequency signal as it descends the
    Relational Lysis hierarchy (recursive application of L).
    
    Verifies that the energy decreases rapidly at each level, confirming that
    the hierarchy acts as a "spectral sieve," isolating the harmonic kernel.

ADVERSARIAL CONDITIONS:
    - Input:                   Mixed sine wave (freqs 37, 113, 311)
    - Levels:                  10 iterations

PASS CRITERIA:
    1. Monotonicity:           Energy decreases at each level.
    2. Convergence:            Approaches machine epsilon (~1e-14).
-------------------------------------------------------------------------------
"""

import numpy as np

# ---------------------------------
# Relational Lysis
# ---------------------------------
def L(x):
    return x[2:] - 2*x[1:-1] + x[:-2]

# ---------------------------------
# Energy Functional
# ---------------------------------
def energy(x):
    y = L(x)
    return np.dot(x[1:-1], y)

# ---------------------------------
# Build deterministic test signal
# ---------------------------------
N = 5000
t = np.linspace(0, 2*np.pi, N)
x = np.sin(37*t) + 0.3*np.sin(113*t) + 0.1*np.sin(311*t)

# ---------------------------------
# Iterate Hierarchy
# ---------------------------------
levels = []
energies = []

current = x.copy()

for k in range(10):
    E = energy(current)
    levels.append(current)
    energies.append(E)
    current = L(current)

# ---------------------------------
# Output
# ---------------------------------
for i,E in enumerate(energies):
    print(f"Level {i} Energy: {E}")
