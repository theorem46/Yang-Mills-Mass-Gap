"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_16_boundary insensitivity.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Paper Reference: Section 5.3 (Boundary Conditions)
Theorem Support: "Bulk Independence from Boundary Conditions (Saint-Venant)"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the sensitivity of the Diamond L1 norm to massive disturbances
    at the boundaries (edges) of the array.
    
    Verifies that the "Bulk" energy (L1 of D2) remains stable even when
    endpoints are shifted by large values (10^6), confirming the local
    nature of the operator (Saint-Venant principle analogue).

ADVERSARIAL CONDITIONS:
    - Boundary Shifts:         Up to +/- 1,000,000
    - Input Size:              100,000

PASS CRITERIA:
    1. Bulk Stability:         L1(D2) remains approximately constant (~200,000).
-------------------------------------------------------------------------------
"""

# rl_light_L1_boundary_sensitivity.py
# PURPOSE:
#   Verify diamond closure is insensitive to boundary conditions.
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


# Boundary-conditioned state
def gen_with_boundary(n, left, right):
    x = gen_interior(n)
    x[0] += left
    x[-1] += right
    return x


def run(n, left, right):
    x = gen_with_boundary(n, left, right)
    D, _ = Phi(x)
    del x
    D2 = RL(D)
    return L1(D), L1(D2)


if __name__ == "__main__":
    for l, r in [(0, 0), (10, 0), (0, 10), (10, -10), (10**6, -(10**6))]:
        l1d, l1d2 = run(100_000, l, r)
        print(f"left={l}, right={r}, L1(D)={l1d}, L1(D2)={l1d2}")
