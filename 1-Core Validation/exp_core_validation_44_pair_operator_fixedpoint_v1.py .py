"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_44_pair_operator_fixedpoint_v1.py .py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 3.7 (Hierarchical Lysis)
Theorem Support: "Existence of Shadow Fixed Points in Integer Smoothing"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    A foundational "Toy Model" experiment. It implements a 3-point integer
    averaging kernel (Alignment Diamond) and computes the residual (Shadow).
    
    The script iterates the decomposition levels to verify that the Shadow
    component (S) stabilizes to a fixed point (S_k == S_k-1) or limits
    towards zero, confirming the attractor dynamics of the operator on
    simple integer sequences.

ADVERSARIAL CONDITIONS:
    - Input:                   Fixed integer sequence [7, 3, 9, 1, 8, 2, 6, 4]
    - Arithmetic:              Integer floor division (//)
    - Boundary:                Averaging endpoints (Dirichlet-like)

PASS CRITERIA:
    1. Convergence:            System detects "SHADOW FIXED POINT REACHED".
    2. Stability:              Shadow trace remains invariant between levels.

USAGE:
    python3 exp_core_val_basic_shadow_fixed_point.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""


# ------------------------------------------------------------
# RL Decomposition
# ------------------------------------------------------------


def alignment_diamond(X):
    n = len(X)
    D = [0] * n
    for i in range(n):
        if i == 0:
            D[i] = (X[i] + X[i + 1]) // 2
        elif i == n - 1:
            D[i] = (X[i - 1] + X[i]) // 2
        else:
            D[i] = (X[i - 1] + X[i] + X[i + 1]) // 3
    return D


def shadow_trace(X, D):
    return [X[i] - D[i] for i in range(len(X))]


def rl_pair(X):
    D = alignment_diamond(X)
    S = shadow_trace(X, D)
    return D, S


# ------------------------------------------------------------
# Utility
# ------------------------------------------------------------


def same(A, B):
    if len(A) != len(B):
        return False
    for i in range(len(A)):
        if A[i] != B[i]:
            return False
    return True


# ------------------------------------------------------------
# Main experiment
# ------------------------------------------------------------


def run():
    X = [7, 3, 9, 1, 8, 2, 6, 4]

    levels = 12

    current = X
    prev_shadow = None

    print("Initial X:")
    print(X)

    for k in range(1, levels + 1):
        D, S = rl_pair(current)

        print("\nLevel", k)
        print("Alignment D:", D)
        print("Shadow S:", S)

        if prev_shadow is not None:
            if same(S, prev_shadow):
                print(">>> SHADOW FIXED POINT REACHED AT LEVEL", k)
                break

        prev_shadow = S
        current = D


# ------------------------------------------------------------

if __name__ == "__main__":
    run()
