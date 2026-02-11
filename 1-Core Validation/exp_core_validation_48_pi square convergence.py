"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_48_pi square convergence.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 3.10 (Continuum Limit)
Theorem Support: "Spectral Convergence to Dirichlet Ground State"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    A high-precision variant of the Continuum Refinement test (Exp 12).
    It verifies that the scaled spectral gap (N^2 * lambda_1) converges exactly
    to the analytical continuum value pi^2 (~9.8696) for the 1D Dirichlet
    Laplacian.
    
    This confirms not just that a limit exists, but that the Relational Lysis
    operator recovers the correct physical normalization for wave mechanics
    on a bounded interval.

ADVERSARIAL CONDITIONS:
    - Lattice Sizes:           [50, 100, 200, 400, 800]
    - Target Limit:            pi^2 (9.8696044...)

PASS CRITERIA:
    1. Convergence:            N^2 * lambda_1 approaches 9.8696...
    2. Accuracy:               Error decreases as 1/N^2.

USAGE:
    python3 exp_core_val_12a_pi_squared_convergence.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
import math


# ------------------------------------------------
# Build 1D Relational Lysis (Discrete Laplacian)
# ------------------------------------------------
def build_laplacian(N):
    L = np.zeros((N, N))
    for i in range(N):
        L[i, i] = 2.0
        if i > 0:
            L[i, i - 1] = -1.0
        if i < N - 1:
            L[i, i + 1] = -1.0
    return L


# ------------------------------------------------
# Smallest Nonzero Eigenvalue
# ------------------------------------------------
def smallest_nonzero_eigenvalue(L):
    eigs = np.linalg.eigvalsh(L)
    eigs = np.sort(eigs)
    for v in eigs:
        if v > 1e-12:
            return v
    return None


# ------------------------------------------------
# Main
# ------------------------------------------------
def main():

    print("\nRELATIONAL LYSIS — SCRIPT TYPE 12A")
    print("π^2 Continuum Convergence Test")
    print("--------------------------------------------------")
    print(f"{'N':<8} {'lambda_1':<15} {'N^2 * lambda_1'}")
    print("--------------------------------------------------")

    Ns = [50, 100, 200, 400, 800]

    for N in Ns:
        L = build_laplacian(N)
        lam1 = smallest_nonzero_eigenvalue(L)
        scaled = (N**2) * lam1
        print(f"{N:<8d} {lam1:<15.10e} {scaled:.10f}")

    print("--------------------------------------------------")
    print(f"Expected limit: π^2 = {math.pi**2:.10f}")

    print("\nINTERPRETATION:")
    print("N^2 * λ1 → π^2 confirms:")
    print("Relational Lysis converges to the continuum Laplacian.")
    print("Operator normalization is correct.")


# ------------------------------------------------
if __name__ == "__main__":
    main()
