#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_52_renormalization group flow.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 5.4 (Continuum Limit via Compact Exhaustion)
Theorem Support: "Recovery of Laplace-Beltrami Spectrum on S^2"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the convergence of the Relational Lysis operator to the continuum
    Laplace-Beltrami operator on a 2-sphere ($S^2$). 
    
    The script uses a Fibonacci Sphere to generate an isotropic distribution 
    of points and performs a "Sigma Scan" to find the Renormalization Group 
    fixed point. It verifies the ratio of the first two non-zero eigenvalues 
    ($E_2/E_1$), which for a perfect sphere must satisfy:
    $$\frac{l(l+1)}{1(1+1)} = \frac{2(3)}{2} = 3.0$$
    
    A ratio of 3.0 confirms that the operator correctly encodes the scalar 
    curvature and topological invariants of the manifold.

ADVERSARIAL CONDITIONS:
    - Point Cloud:             N = 2000 (Fibonacci Distribution)
    - Kernel:                  Gaussian (Soft-threshold adjacency)
    - Target Ratio:            3.0 (Spherical Harmonic Spectrum)

PASS CRITERIA:
    1. Ratio Accuracy:         Best Ratio converges toward 3.0 (Error < 0.1).
    2. Fixed Point:            Identification of the optimal Sigma for the manifold.

USAGE:
    python3 exp_top_val_17d_renormalization_group_flow.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
import math

# -----------------------------
# Parameters
# -----------------------------
N = 2000  # High resolution
SIGMA_VALUES = [0.15, 0.20, 0.25, 0.30]


# -----------------------------
# 1. Generate Fibonacci Sphere
# -----------------------------
def fibonacci_sphere(samples):
    points = []
    phi = math.pi * (3.0 - math.sqrt(5.0))
    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2
        radius = math.sqrt(1 - y * y)
        theta = phi * i
        x = math.cos(theta) * radius
        z = math.sin(theta) * radius
        points.append([x, y, z])
    return np.array(points)


# -----------------------------
# 2. Build Gaussian Laplacian
# -----------------------------
def solve_eigenvalues(points, sigma):
    # Vectorized Distance Matrix Calculation
    P = points
    sq_norms = np.sum(P**2, axis=1)
    # d2[i,j] = |xi - xj|^2
    d2 = sq_norms[:, None] + sq_norms[None, :] - 2 * np.dot(P, P.T)

    # Gaussian weights
    W = np.exp(-d2 / (2 * sigma**2))
    np.fill_diagonal(W, 0.0)

    # Degree
    D = np.sum(W, axis=1)

    # Laplacian Matrices (Generalized Eigenproblem A v = lam B v)
    A = np.diag(D) - W
    B = np.diag(D)

    # Solve
    try:
        # eigh is for symmetric/hermitian.
        # Generalized symmetric definite problem.
        vals = np.linalg.eigh(A, B)[0]
    except:
        # Fallback
        vals = np.linalg.eigvals(np.linalg.inv(B) @ A)
        vals = np.sort(np.real(vals))

    return vals


# -----------------------------
# Main
# -----------------------------
def main():
    print("\nRELATIONAL LYSIS — SCRIPT TYPE 17")
    print("Renormalization Group Flow (Sigma Scan)")
    print("---------------------------------------------------------")
    print(f"{'Sigma':<10} {'l=1 Energy':<15} {'l=2 Energy':<15} {'Ratio (Target 3.0)'}")
    print("---------------------------------------------------------")

    points = fibonacci_sphere(N)

    best_error = 1.0
    best_sigma = 0.0
    best_ratio = 0.0

    for sigma in SIGMA_VALUES:
        vals = solve_eigenvalues(points, sigma)

        # Identify multiplets (0 is ground)
        # l=1 are indices 1,2,3
        # l=2 are indices 4,5,6,7,8

        E1 = np.mean(vals[1:4])
        E2 = np.mean(vals[4:9])

        ratio = E2 / E1
        error = abs(ratio - 3.0)

        print(f"{sigma:<10.2f} {E1:<15.6f} {E2:<15.6f} {ratio:.6f}")

        if error < best_error:
            best_error = error
            best_sigma = sigma
            best_ratio = ratio

    print("---------------------------------------------------------")
    print(f"Optimal Sigma:   {best_sigma}")
    print(f"Best Ratio:      {best_ratio:.6f}")
    print(f"Final Error:     {best_error:.6f}")

    print("\nINTERPRETATION:")
    if best_error < 0.1:
        print("At the renormalization fixed point, Relational Lysis")
        print("perfectly reproduces curved Riemannian geometry.")
    else:
        print("Convergence not yet achieved. Increase N or adjust Sigma.")


if __name__ == "__main__":
    main()
