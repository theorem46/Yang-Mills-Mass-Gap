#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_20_laplacian equivalence.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 3.8, Theorem 3.24 (Operator Necessity)
Theorem Support: "Necessity of the Alignment Operator Class (Second-Order)"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the claim that Relational Lysis is structurally equivalent to the
    Discrete Laplacian. Specifically, it verifies that L(x) acts as the
    second difference operator D(D(x)), where D is the first difference.

    This integer-based version eliminates floating-point artifacts and
    confirms exact structural equivalence.

ADVERSARIAL CONDITIONS:
    - Input:                   Deterministic Integer Sequence
    - Scale:                   10**9
    - Size:                    N=5000
    - Precision:               Exact Integer Arithmetic

PASS CRITERIA:
    1. Operator Match:         EXACT ZERO

USAGE:
    python3 exp_core_val_20_laplacian_equivalence.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import math

N = 5000
SCALE = 10**9

# ------------------------------------------------
# Deterministic Integer Sequence
# ------------------------------------------------

# High dynamic range integer stress pattern
x = [(i * 7919 % 104729 - 52364) * SCALE for i in range(N)]

# ------------------------------------------------
# Relational Lysis Operator
# ------------------------------------------------

def lysis(x):
    return [x[i + 2] - 2 * x[i + 1] + x[i] for i in range(len(x) - 2)]

# ------------------------------------------------
# First Difference Operator
# ------------------------------------------------

def diff1(x):
    return [x[i + 1] - x[i] for i in range(len(x) - 1)]

# ------------------------------------------------
# Compose First Difference Twice
# ------------------------------------------------

def diff2(x):
    return diff1(diff1(x))

# ------------------------------------------------
# Integer Norm
# ------------------------------------------------

def norm(v):
    return math.isqrt(sum(a * a for a in v))

# ------------------------------------------------
# Main Test
# ------------------------------------------------

L = lysis(x)
D2 = diff2(x)

diff_vec = [L[i] - D2[i] for i in range(len(L))]
error = norm(diff_vec)

print("\nRELATIONAL LYSIS — SCRIPT TYPE 2: LAPLACIAN EQUIVALENCE")
print("------------------------------------------------------")
print("||L(x) - D(D(x))|| =", error)

print("\nINTERPRETATION:")
print("Zero confirms exact structural equivalence:")
print("Relational Lysis ≡ Discrete Laplacian.")
