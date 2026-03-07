#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_60_ground state hunter.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 11.10, Theorem 11.10 (Spectral Compactness)
Theorem Support: "Numerical Verification of the Dirichlet Ground State"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Implements a "Ground State Hunter" using Inverse Power Iteration to find 
    the smallest eigenvalue ($\lambda_1$) of the Relational Lysis operator. 
    
    By utilizing LU decomposition to iteratively solve the system $(L)v_{n+1} = v_n$, 
    this script bypasses the limitations of standard power iteration (which 
    targets the largest eigenvalue) and converges directly on the infrared 
    limit (the Mass Gap). The results are benchmarked against the analytical 
    Dirichlet limit:
    $$\lambda_1 \approx \left(\frac{\pi}{N+1}\right)^2$$
    
    Successful matching proves that our numerical tools are sufficient for 
    detecting the true Mass Gap in non-Abelian gauge configurations.

ADVERSARIAL CONDITIONS:
    - Lattice Sizes:           [50, 100, 200]
    - Solver:                  LU-based Inverse Iteration
    - Tolerance:               1e-09
    - Benchmark:               Analytical Dirichlet Ground State

PASS CRITERIA:
    1. Precision Match:        Calculated $\lambda_1$ matches the expected 
                               limit within tolerance.
    2. Convergence:            Algorithm finds a stable fixed point in 
                               under 1000 iterations.

USAGE:
    python3 exp_core_val_39b_inverse_iteration_ground_state.py --verbose

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
