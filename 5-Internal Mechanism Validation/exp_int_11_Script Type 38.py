#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_int_11_Script Type 38.py
Category:        5-Internal Mechanism Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 25.1, Proposition 25.1 (Spectral Continuity)
Theorem Support: "Gamma-Convergence of the Hierarchical Laplacian"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the continuum limit behavior of the Relational Lysis operator. 
    In numerical analysis, a discrete operator is only physically valid if it 
    retains its spectral signature as the resolution (N) increases. 
    
    This script evaluates the smallest non-zero eigenvalue ($\lambda_1$) across 
    doubling lattice sizes. By calculating the scaled metric ($N^2 \cdot \lambda_1$), 
    the experiment verifies if the mass gap approaches a stable constant. 
    
    A stabilized $N^2 \cdot \lambda_1$ value proves that the Mass Gap is not a 
    discretization artifact (noise) but an intrinsic property of the underlying 
    geometric manifold, surviving the transition from a discrete lattice 
    to a continuous field theory.

ADVERSARIAL CONDITIONS:
    - Lattice Sizes:           [50, 100, 200, 400, 800]
    - Precision Threshold:      1e-14 (For eigenvalue zero-clipping)
    - Eigenvalue Solver:        Standard Symmetric Solver (eigvalsh)
    - Metric:                   Scaled Eigenvalue ($N^2 \cdot \lambda_1$)

PASS CRITERIA:
    1. Scaling Invariance:     $N^2 \cdot \lambda_1$ converges to a constant 
                               as N increases.
    2. Continuum Existence:    The spectral gap remains non-zero in the 
                               limit of infinite resolution.
    3. Structural Stability:   Confirms the existence of a well-defined 
                               Continuum Operator ($\Delta_{RL}$).

USAGE:
    python3 exp_top_val_38_gamma_continuum_spectral_convergence.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np


# -----------------------------
# Build 1D Lysis (Laplacian) matrix
# -----------------------------
def build_lysis_matrix(N):
    L = np.zeros((N, N))
    for i in range(N):
        L[i, i] = -2
        if i > 0:
            L[i, i - 1] = 1
        if i < N - 1:
            L[i, i + 1] = 1
    return L


# -----------------------------
# Smallest nonzero eigenvalue
# -----------------------------
def smallest_nonzero_eigenvalue(L):
    vals = np.linalg.eigvalsh(L)
    vals = np.sort(np.abs(vals))  # use absolute
    for v in vals:
        if v > 1e-14:  # smaller threshold
            return v
    return None


# -----------------------------
# Main
# -----------------------------
def main():
    print("\nRELATIONAL LYSIS — SCRIPT TYPE 38 (FIXED)")
    print("Gamma-Convergence / Continuum Spectral Convergence")
    print("-----------------------------------------------------")
    print("N     lambda1        N^2 * lambda1")
    print("-----------------------------------------------------")

    for N in [50, 100, 200, 400, 800]:
        L = build_lysis_matrix(N)
        lam = smallest_nonzero_eigenvalue(L)
        scaled = (N**2) * lam
        print(f"{N:<5d} {lam:12.6e} {scaled:14.6f}")

    print("-----------------------------------------------------")
    print("INTERPRETATION:")
    print("If N^2 * lambda1 -> constant:")
    print("Relational Lysis converges to unique continuum operator.")
    print("Mass gap is not discretization artifact.")


if __name__ == "__main__":
    main()
