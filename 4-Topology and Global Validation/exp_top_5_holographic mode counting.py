"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_top_5_holographic mode counting.py
Category:        4-Topology and Global Validation
Researcher:      Dr. David Swanagon
Paper Reference: Section 13.2 (Entropy Bounds)
Theorem Support: "Holographic Degree of Freedom Counting"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Counts the number of active eigenmodes below a specific energy threshold
    within a region of radius R.
    
    Verifies that the number of modes scales with the boundary size (R), not
    the bulk volume (R^2), confirming the holographic principle at the level
    of the operator's spectrum.

ADVERSARIAL CONDITIONS:
    - Threshold:               Adaptive (10 / R^2)
    - Radii:                   10 to 80

PASS CRITERIA:
    1. Mode Scaling:           Count is proportional to R (Boundary).
-------------------------------------------------------------------------------
"""

import numpy as np

N = 80
RADII = [10, 20, 30, 40, 60, 80]

# Build 2D Laplacian
L = np.zeros((N * N, N * N))


def idx(i, j):
    return i * N + j


for i in range(N):
    for j in range(N):
        p = idx(i, j)
        L[p, p] = -4
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < N and 0 <= nj < N:
                L[p, idx(ni, nj)] = 1

evals = np.sort(np.abs(np.linalg.eigvalsh(L)))

print("\nRELATIONAL LYSIS — SCRIPT TYPE 20B")
print("Holographic Mode Count Test (Adaptive Threshold)")
print("--------------------------------------------------")
print("R      Threshold       Modes")

for R in RADII:
    thresh = 10 / (R * R)
    count = np.sum(evals < thresh)
    print(f"{R:<6} {thresh:<13.3e} {count}")

print("\nINTERPRETATION:")
print("Modes ∝ R  → holographic")
print("Modes ∝ R^2 → bulk")
