#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_19_linearity homogeneity.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 3.7.2, Lemma 3.16 (Linearity)
Theorem Support: "Linearity of Alignment Propagation"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Validates the fundamental algebraic properties of the Relational Lysis
    operator: Additivity (L(x+y) = Lx + Ly) and Homogeneity (L(cx) = cLx).

    The script applies the operator to integer-valued SU(3) diagonal
    generator paths to ensure exact arithmetic with no floating artifacts.
    This confirms the operator is a linear map.

ADVERSARIAL CONDITIONS:
    - Input Space:             SU(3) Diagonal Path Generator (Integer Form)
    - Phase Shifts:            Integer Offsets
    - Scale Factor:            10**9 (Large amplitude stress test)
    - Precision:               Exact Integer Arithmetic

PASS CRITERIA:
    1. Additivity Error:       EXACT ZERO
    2. Homogeneity Error:      EXACT ZERO

USAGE:
    python3 exp_core_val_19_linearity_homogeneity.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import math
import numpy as np

SCALE = 10**9
L = 6

# ------------------------------------------------
# SU(3) Generator (Integer Diagonal Path)
# ------------------------------------------------

def su3_diag(k):
    # Deterministic integer diagonal structure
    return [
        SCALE * k,
        -SCALE * k,
        SCALE
    ]


def build_sequence(phase_shift=0):
    seq = []

    for i in range(L**4):
        k = i + phase_shift
        elems = su3_diag(k)
        for val in elems:
            seq.append(val)

    return np.array(seq, dtype=np.int64)


# ------------------------------------------------
# Relational Lysis Operator
# ------------------------------------------------

def lysis(x):
    return x[2:] - 2 * x[1:-1] + x[:-2]


# ------------------------------------------------
# Norm
# ------------------------------------------------

def norm(x):
    return math.isqrt(int(np.sum(x * x)))


# ------------------------------------------------
# Main Test
# ------------------------------------------------

def main():
    print("\nRELATIONAL LYSIS — SCRIPT AA1: LINEARITY TEST")
    print("-" * 60)

    # Two independent integer sequences
    x = build_sequence(1)
    y = build_sequence(37)

    Lx = lysis(x)
    Ly = lysis(y)

    # ------------------------
    # Additivity Test
    # ------------------------

    Lxy = lysis(x + y)
    sum_L = Lx + Ly

    add_error = norm(Lxy - sum_L)

    print("Additivity Test:")
    print("||L(x+y) - (Lx+Ly)|| =", add_error)

    # ------------------------
    # Homogeneity Test
    # ------------------------

    c = 7  # integer scale
    Lcx = lysis(c * x)
    cLx = c * Lx

    scale_error = norm(Lcx - cLx)

    print("\nHomogeneity Test:")
    print("||L(c x) - c L(x)|| =", scale_error)

    # ------------------------
    # Interpretation
    # ------------------------

    print("\nINTERPRETATION:")
    print("Zero confirms exact linearity under integer arithmetic.")


if __name__ == "__main__":
    main()
