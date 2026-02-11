"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_47_continium refinement.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 3.10 (Continuum Limit)
Theorem Support: "Gamma-Convergence to Continuum Laplacian"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the convergence of the discrete Relational Lysis operator to the
    continuum operator as the lattice is refined (N increases).
    
    It calculates the smallest non-zero eigenvalue (lambda_1) for increasing N.
    Stability or predictable scaling of this value indicates that the discrete
    sequence of functionals converges to a well-defined continuum functional
    (the Dirichlet Energy).

ADVERSARIAL CONDITIONS:
    - Lattice Sizes:           [50, 100, 200, 400, 800]
    - Metric:                  Smallest nonzero eigenvalue

PASS CRITERIA:
    1. Convergence:            Lambda_1 scales predictably toward the continuum limit.
    2. Stability:              No divergence or erratic behavior as N -> Infinity.

USAGE:
    python3 exp_core_val_12_continuum_refinement.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""
import numpy as np
import math

# ------------------------------------------
# Build Relational Lysis (1D Laplacian) Matrix
# ------------------------------------------


def build_lysis_matrix(N):
    L = np.zeros((N, N))
    for i in range(1, N - 1):
        L[i, i - 1] = 1.0
        L[i, i] = -2.0
        L[i, i + 1] = 1.0
    return -L  # positive Laplacian


# ------------------------------------------
# Smallest nonzero eigenvalue
# ------------------------------------------


def smallest_nonzero_eigenvalue(A):
    eigs = np.linalg.eigvalsh(A)
    eigs = np.sort(eigs)
    for v in eigs:
        if v > 1e-10:
            return v
    return None


# ------------------------------------------
# Main
# ------------------------------------------


def main():
    print("\nRELATIONAL LYSIS — SCRIPT TYPE 12")
    print("Continuum Refinement Scaling")
    print("--------------------------------------------------")
    print(f"{'N':<8} {'lambda_1'}")

    Ns = [50, 100, 200, 400, 800]

    for N in Ns:
        L = build_lysis_matrix(N)
        lam = smallest_nonzero_eigenvalue(L)
        print(f"{N:<8d} {lam:.10f}")

    print("\nINTERPRETATION:")
    print("lambda_1 should converge toward a constant")
    print("as N increases → continuum limit.")


if __name__ == "__main__":
    main()
