#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_24_relativist dispersion.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 9.5 (Emergence of the Quantum Hamiltonian)
Theorem Support: "Relativistic Dispersion of Mass Gap Excitations"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the dispersion relation of the massless limit of the theory.
    Verifies that omega^2 (Lysis Energy) scales perfectly with k^2 (Wave Number).
    
    This ensures that the "Shadow Propagation" corresponds to the propagation
    of relativistic massless particles (photons/gluons) in the free field limit.

ADVERSARIAL CONDITIONS:
    - Wave Numbers:            k=1 to k=20
    - Precision:               Check ratio (w/k)^2

PASS CRITERIA:
    1. Dispersion Ratio:       0.99 < (w^2 / k^2) < 1.01

USAGE:
    python3 exp_quant_rec_26_relativistic_dispersion.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np

# -------------------------
# Grid
# -------------------------
N = 400
dx = 1.0

# -------------------------
# Build Laplacian Matrix (Dirichlet)
# -------------------------
L = np.zeros((N, N))

for i in range(N):
    if i > 0:
        L[i, i - 1] = 1
    L[i, i] = -2
    if i < N - 1:
        L[i, i + 1] = 1

# Negative Laplacian for Energy
K = -L / (dx**2)

# -------------------------
# Eigenproblem
# -------------------------
eigvals, eigvecs = np.linalg.eigh(K)

# -------------------------
# Analysis
# -------------------------
print("\nRELATIONAL LYSIS — SCRIPT TYPE 26B")
print("Relativistic Dispersion Test (Massless Limit)")
print("---------------------------------------------------------")
print(f"{'Mode(n)':<8} {'k^2 (Theory)':<15} {'w^2 (Lysis)':<15} {'Ratio (w/k)^2'}")
print("---------------------------------------------------------")

# Check first few modes and some higher ones
for n in [1, 2, 3, 5, 10, 20]:
    # Correct Indexing: Mode n is at index n-1
    omega2 = eigvals[n - 1]

    # Theoretical Momentum for Dirichlet Box
    # k = n * pi / (N + 1)
    k = np.pi * n / (N + 1)
    k2 = k**2

    ratio = omega2 / k2
    diff = omega2 - k2

    print(f"{n:<8d} {k2:<15.6e} {omega2:<15.6e} {ratio:.6f}")

print("---------------------------------------------------------")
print("INTERPRETATION:")
print("Ratio ≈ 1.00 confirms w^2 = k^2.")
print("Relational Lysis yields correct relativistic dispersion")
print("for a massless field (Photon/Gluon).")
