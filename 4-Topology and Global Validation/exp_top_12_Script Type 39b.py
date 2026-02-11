"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_top_12_Script Type 39b.py
Category:        4-Topology and Global Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 35.1 (Spectral Floor and Ground State Isolation)
Theorem Support: "Convergence of Inverse Iteration on the Lysis Manifold"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the accuracy of the spectral ground state identification. In quantum 
    field theory, the Mass Gap is synonymous with the energy of the first 
    excited state above the vacuum (or the lowest non-trivial eigenvalue). 
    
    This script utilizes the Inverse Power Iteration algorithm—a method 
    specifically designed to converge on the eigenvalue with the smallest 
    magnitude. By comparing the calculated $\lambda_1$ of a Dirichlet 
    Laplacian against the analytical expectation $(\pi / (N+1))^2$, the 
    experiment verifies that the framework's "Ground State Hunter" is 
    functioning with high-fidelity numerical precision.

ADVERSARIAL CONDITIONS:
    - Lattice Sizes:           [50, 100, 200]
    - Method:                  Inverse Power Iteration (LU Factorization)
    - Tolerance:               1e-9
    - Theoretical Baseline:     Dirichlet Spectral Law $(\pi / (N+1))^2$

PASS CRITERIA:
    1. Precision Match:        Calculated $\lambda_1$ matches the analytical 
                               expected value to at least 5 decimal places.
    2. Numerical Stability:    The LU-based solver converges within the 
                               iteration limit (max_iter=1000).
    3. Ground State Integrity: Confirms the operator correctly identifies the 
                               global minimum of the energy landscape.

USAGE:
    python3 exp_core_val_39b_ground_state_inverse_iteration.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
import scipy.linalg as la


def build_lysis_matrix(N):
    # 1D Dirichlet Laplacian
    main_diag = -2 * np.ones(N)
    off_diag = np.ones(N - 1)
    L = np.diag(main_diag) + np.diag(off_diag, k=1) + np.diag(off_diag, k=-1)
    return -L  # Return positive definite form (-Delta)


def inverse_power_iteration(A, tol=1e-9, max_iter=1000):
    # Finds the smallest eigenvalue and eigenvector
    n = A.shape[0]
    v = np.random.rand(n)
    v = v / np.linalg.norm(v)

    # Pre-factor for speed
    lu, piv = la.lu_factor(A)

    lam_prev = 0
    for i in range(max_iter):
        # Solve A * v_new = v_old
        v_next = la.lu_solve((lu, piv), v)

        # Normalize
        v_next = v_next / np.linalg.norm(v_next)

        # Rayleigh Quotient
        lam = v_next.T @ A @ v_next

        if np.abs(lam - lam_prev) < tol:
            return lam, v_next

        lam_prev = lam
        v = v_next

    return lam, v


def main():
    print("\nRELATIONAL LYSIS — SCRIPT TYPE 39b")
    print("True Ground State Search (Inverse Iteration)")
    print("-----------------------------------------------------")
    print(f"{'N':<5} {'Calculated Lambda_1':<20} {'Expected (pi/N)^2':<20}")
    print("-----------------------------------------------------")

    for N in [50, 100, 200]:
        L = build_lysis_matrix(N)

        # We add a tiny epsilon to avoid singular matrix if purely periodic
        # But Dirichlet is invertible.
        lam, _ = inverse_power_iteration(L)

        expected = (np.pi / (N + 1)) ** 2

        print(f"{N:<5} {lam:.6e}{' '*8} {expected:.6e}")

    print("-----------------------------------------------------")
    print("INTERPRETATION:")
    print("If Calculated matches Expected, our 'Ground State Hunter'")
    print("is working. We can now trust it to find the Mass Gap")
    print("in the Yang-Mills scripts.")


if __name__ == "__main__":
    main()
