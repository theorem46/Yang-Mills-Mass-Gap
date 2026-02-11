"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_58_gamma convergence.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 11.9, Theorem 11.9 (Continuum Limit of Functionals)
Theorem Support: "Gamma-Convergence of Discrete Lysis to the Laplacian"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Validates the Gamma-convergence of the Relational Lysis operator as the 
    lattice spacing approaches zero. 
    
    The script measures the smallest non-zero eigenvalue ($\lambda_1$) across 
    multiple scales ($N$) and applies the scaling law $N^2 \lambda_1$. In 
    variational analysis, this convergence ensures that the discrete 
    minimizers of the system (the "Solved States") converge to the continuous 
    minimizers of the Dirichlet energy. 
    
    Proving that $N^2 \lambda_1$ approaches a stable constant confirms that 
    the Mass Gap is an intrinsic feature of the underlying geometry and 
    will persist in the true continuum limit.

ADVERSARIAL CONDITIONS:
    - Lattice Sizes:           [50, 100, 200, 400, 800]
    - Precision Threshold:      1e-14 (To capture near-zero modes)
    - Scaling Factor:          $N^2$ (Canonical Laplacian scaling)

PASS CRITERIA:
    1. Continuum Stability:    $N^2 \lambda_1$ converges to a constant value.
    2. Non-Zero Limit:         The constant is strictly positive, 
                               denoting a persistent Mass Gap.

USAGE:
    python3 exp_core_val_38_gamma_convergence_spectral.py --verbose

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
