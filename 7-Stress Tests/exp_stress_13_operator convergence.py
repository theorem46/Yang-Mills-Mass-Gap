"""
RELATIONAL LYSIS — OPERATOR CONVERGENCE TEST (Corrected)
Appendix B Validation
"""

import numpy as np
from scipy.linalg import eigh


# ============================================================
# Discrete Laplacian with proper scaling
# ============================================================

def laplacian_matrix(n):

    h = 1.0 / (n - 1)

    L = np.zeros((n, n))

    for i in range(n):

        if i > 0:
            L[i, i-1] = -1

        if i < n-1:
            L[i, i+1] = -1

        L[i, i] = 2

    return L / (h**2)


# ============================================================
# Experiment
# ============================================================

def run():

    sizes = [32, 64, 128, 256]

    print("\nRELATIONAL LYSIS — OPERATOR CONVERGENCE TEST\n")

    for n in sizes:

        L = laplacian_matrix(n)

        vals = eigh(L, eigvals_only=True)

        smallest_nonzero = vals[1]

        print(f"n={n}, smallest nonzero eigenvalue={smallest_nonzero}")


if __name__ == "__main__":
    run()