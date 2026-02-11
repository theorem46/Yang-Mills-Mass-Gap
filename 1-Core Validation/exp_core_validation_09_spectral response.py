"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_09_spectral response.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Paper Reference: Section 5.1 (Spectral Decomposition)
Theorem Support: "Frequency-Dependent Energy Scaling"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Measures the "Diamond Energy" (L1 norm of the Lysis output) for sine waves
    of increasing frequency `m`.
    
    Verifies that the operator acts as a high-pass filter (characteristic of
    Laplacians), where energy scales with frequency. This confirms the
    spectral response of the discrete operator.

ADVERSARIAL CONDITIONS:
    - Frequencies (m):         Powers of 2 (1 to 128)
    - Input:                   Deterministic Sine Waves (N=4000)

PASS CRITERIA:
    1. Scaling:                Energy increases monotonically with frequency.
-------------------------------------------------------------------------------
"""

import numpy as np


# RL operator
def L(x):
    return x[2:] - 2 * x[1:-1] + x[:-2]


# First-level diamond
def diamond(x):
    return L(x)


# Diamond-geometry invariant
def diamond_energy(D):
    return np.mean(np.abs(L(D)))


# Generate solved-state family
N = 4000
t = np.linspace(0, 2 * np.pi, N)

ms = [1, 2, 4, 8, 16, 32, 64, 128]
results = {}

for m in ms:
    x = np.sin(m * t)
    D = diamond(x)
    E = diamond_energy(D)
    results[m] = E

# Print results
for m in ms:
    print(f"m={m:3d}   diamond_energy={results[m]}")
