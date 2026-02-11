"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_17_light scale invariance.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Paper Reference: Section 3.10 (Continuum Limit)
Theorem Support: "Stride Invariance / Scale Independence"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the operator's behavior under subsampling (Stride-k).
    Verifies that the geometric structure (Diamond closure) persists
    regardless of the sampling rate, a requirement for continuum limits.

ADVERSARIAL CONDITIONS:
    - Strides:                 1, 2, 4, 8
    - Input Size:              1,000,000

PASS CRITERIA:
    1. Scaling:                L1 Energy scales predictably with length reduction.
-------------------------------------------------------------------------------
"""

# rl_light_L2_stride_variation.py
# PURPOSE:
#   Verify diamond closure is invariant under lattice stride-k subsampling.
# CONSTRAINTS:
#   Deterministic, integer-only, diamond-only computation.

import numpy as np


def RL(x):
    return x[2:] - 2 * x[1:-1] + x[:-2]


def Phi(x):
    D = RL(x)
    S = x[1:-1] - D
    return D, S


def L1(x):
    return int(np.sum(np.abs(x)))


# Admissible interior generator
def gen_interior(n):
    i = np.arange(n, dtype=np.int64)
    return (i * i * i + 5 * i * i + 13) // 7


# Stride-k subsampling
def stride(x, k):
    return x[::k]


def run(n, k):
    x = gen_interior(n)
    xk = stride(x, k)
    D, _ = Phi(xk)
    del x, xk
    D2 = RL(D)
    return L1(D), L1(D2), len(D), len(D2)


if __name__ == "__main__":
    for k in [1, 2, 4, 8]:
        l1d, l1d2, ld, ld2 = run(1_000_000, k)
        print(f"stride={k}, D_len={ld}, D2_len={ld2}, L1(D)={l1d}, L1(D2)={l1d2}")
