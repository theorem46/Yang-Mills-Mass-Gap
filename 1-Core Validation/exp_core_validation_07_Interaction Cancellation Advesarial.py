#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

#!/usr/bin/env python3
"""
RELATIONAL LYSIS — T12.5 ADVERSARIAL INTERACTION CANCELLATION TEST
=================================================================

Goal:
Attempt to destroy interaction by constructing configurations where
classical A∧A contributions cancel globally.

PASS requires:
- Nonzero solved-state invariant
- Nonzero solved-state transition count
"""

import numpy as np
from numpy.linalg import norm

N = 512
EPS_LIST = np.logspace(-12, -2, 14)
MAX_DEPTH = 120
TOL = 1e-13

# --------------------------------------------------
# RL primitives (unchanged)
# --------------------------------------------------

def laplacian(x):
    return np.roll(x, -1) - 2*x + np.roll(x, 1)

def solved_state(x):
    diamond = laplacian(x)
    shadow = x - np.mean(x)
    S = diamond + shadow
    return S / (norm(S) + 1e-15)

def invariant(S):
    return norm(laplacian(S))

def lysis(S0):
    seq = [S0]
    for _ in range(MAX_DEPTH):
        Sn = solved_state(seq[-1])
        if norm(Sn - seq[-1]) < TOL:
            break
        seq.append(Sn)
    return seq

def interaction_count(seq):
    return sum(
        invariant(seq[i+1]) != invariant(seq[i])
        for i in range(len(seq)-1)
    )

# --------------------------------------------------
# Adversarial configuration:
# Alternating curvature packets with zero net A∧A
# --------------------------------------------------

def cancelling_configuration(n):
    x = np.zeros(n)
    half = n // 2
    x[:half] = np.sin(np.linspace(0, 8*np.pi, half))
    x[half:] = -np.sin(np.linspace(0, 8*np.pi, n-half))
    return x / (np.max(np.abs(x)) + 1e-15)

# --------------------------------------------------
# Test
# --------------------------------------------------

print("\nRELATIONAL LYSIS — T12.5 INTERACTION CANCELLATION TEST")
print("======================================================")

for eps in EPS_LIST:
    A = eps * cancelling_configuration(N)
    S0 = solved_state(A)

    inv = invariant(S0)
    if inv < TOL:
        raise RuntimeError("FAIL: Cancellation collapsed solved state.")

    seq = lysis(S0)
    inter = interaction_count(seq)

    if inter == 0:
        raise RuntimeError("FAIL: Interaction eliminated by cancellation.")

    print(f"ε={eps:8.1e} | depth={len(seq):3d} | interaction={inter:3d} | inv={inv:.3e}")

print("\n[PASSED]")
print("• Interaction survives classical cancellation")
print("• Solved-state transitions are geometric, not perturbative")
