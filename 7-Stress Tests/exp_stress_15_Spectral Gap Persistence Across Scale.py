"""
RELATIONAL LYSIS — SPECTRAL GAP TEST (Corrected)
Appendix D Validation
"""

import numpy as np
from scipy.linalg import eigh


# ============================================================
# Scaled Laplacian
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

    sizes = [32, 64, 128, 256, 512]
    gaps = []

    print("\nRELATIONAL LYSIS — SPECTRAL GAP TEST\n")

    for n in sizes:

        L = laplacian_matrix(n)

        vals = eigh(L, eigvals_only=True)

        # remove zero mode if present
        vals = vals[vals > 1e-10]

        gap = vals[0]
        gaps.append(gap)

        print(f"n={n}, spectral gap={gap}")

    print("\nGaps:", gaps)


if __name__ == "__main__":
    run()