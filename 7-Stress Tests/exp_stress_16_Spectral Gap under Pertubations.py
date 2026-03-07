"""
RELATIONAL LYSIS — SPECTRAL GAP UNDER PERTURBATIONS (Tier-1)

Script: exp_16_gap_perturbation.py
Category:        7-Stress Tests
Paper Reference: Appendix D (Mass Gap Support)

Purpose
-------
Test whether the smallest nonzero eigenvalue (spectral gap)
remains bounded under random operator perturbations.

This evaluates robustness of coercivity.
"""

import numpy as np
from scipy.linalg import eigh
import time


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
# Random Symmetric Perturbation
# ============================================================

def random_perturbation(n, strength):

    A = np.random.randn(n, n)
    A = (A + A.T) / 2.0

    return strength * A


# ============================================================
# Gap Computation
# ============================================================

def spectral_gap(M):

    vals = eigh(M, eigvals_only=True)

    vals = vals[vals > 1e-10]

    return vals[0]


# ============================================================
# Experiment
# ============================================================

def run():

    print("\n====================================================")
    print("RELATIONAL LYSIS — SPECTRAL GAP PERTURBATION TEST")
    print("Tier-1 Validation")
    print("====================================================\n")

    start = time.time()

    sizes = [64, 128, 256]
    perturb_strengths = [0.01, 0.05, 0.1]
    trials = 10

    for n in sizes:

        print(f"\n--- Resolution n = {n} ---")

        base_L = laplacian_matrix(n)
        base_gap = spectral_gap(base_L)

        print(f"Base Gap: {base_gap:.6f}")

        for eps in perturb_strengths:

            gaps = []

            for _ in range(trials):

                P = random_perturbation(n, eps)
                M = base_L + P

                gap = spectral_gap(M)
                gaps.append(gap)

            gaps = np.array(gaps)

            print(f"\nPerturbation Strength {eps}")
            print(f"Mean Gap : {np.mean(gaps):.6f}")
            print(f"Std Dev  : {np.std(gaps):.6f}")
            print(f"Min/Max  : {gaps.min():.6f} / {gaps.max():.6f}")

    print("\n====================================================")
    print("EXECUTION COMPLETE")
    print(f"Total Time: {time.time() - start:.2f} sec")
    print("====================================================\n")


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    run()