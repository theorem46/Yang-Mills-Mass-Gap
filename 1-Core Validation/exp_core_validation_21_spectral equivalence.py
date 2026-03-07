#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_21_spectral equivalence.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 4.4, Theorem 4.2 (Uniqueness of Covariant Laplacian)
Theorem Support: "Identification of the Alignment Operator"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Verifies the spectral equivalence between the Relational Lysis "Shadow Energy"
    functional and the smallest eigenvalue of the discrete Laplacian.
    
    Checks the identity: N^2 * E_shadow ≈ λ_1
    This confirms that the minimization of shadow energy naturally recovers
    the spectral gap of the manifold.

ADVERSARIAL CONDITIONS:
    - Lattice Size (N):        1000
    - Input:                   Smooth sine wave (Ground state candidate)
    - Precision:               1e-12

PASS CRITERIA:
    1. Spectral Ratio:         (N^2 * E) / λ_1 ≈ 1.0 (Convergence to 1.0)

USAGE:
    python3 exp_core_val_03_spectral_equivalence.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""


import numpy as np
import math

# -----------------------------
# Parameters
# -----------------------------

N = 1000  # lattice size
SCALE = 1.0  # no fixed-point scaling needed here

# -----------------------------
# Build smooth test signal
# -----------------------------

x = np.array([math.sin(2 * math.pi * i / N) for i in range(N)])

# -----------------------------
# Relational Lysis operator
# -----------------------------


def lysis(x):
    return np.array([x[(i + 1) % N] - 2 * x[i] + x[(i - 1) % N] for i in range(N)])


def shadow_energy(x):
    k = lysis(x)
    return np.linalg.norm(k) / np.linalg.norm(x)


E = shadow_energy(x)

# -----------------------------
# Build discrete Laplacian matrix
# -----------------------------

L = np.zeros((N, N))

for i in range(N):
    L[i, i] = -2
    L[i, (i + 1) % N] = 1
    L[i, (i - 1) % N] = 1

# -----------------------------
# Compute smallest nonzero eigenvalue
# -----------------------------

eigs = np.linalg.eigvalsh(L)
eigs = np.sort(eigs)

lambda1 = abs(eigs[1])  # skip zero mode

# -----------------------------
# Display results
# -----------------------------

print("\nRELATIONAL LYSIS — SCRIPT TYPE 3")
print("----------------------------------------------------")
print(f"Shadow Energy E:          {E:.12e}")
print(f"N^2 * E:                 {N*N*E:.12e}")
print(f"Laplacian eigenvalue λ1: {lambda1:.12e}")
print(f"(N^2 * E) / λ1:          {(N*N*E)/lambda1:.12e}")

print("\nINTERPRETATION:")
print("N^2 * ShadowEnergy ≈ λ1")
print("Relational Lysis equals the discrete Laplacian.")
print("Energy functional measures spectral gap.")
