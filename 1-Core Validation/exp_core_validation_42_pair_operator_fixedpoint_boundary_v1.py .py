#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_42_pair_operator_fixedpoint_boundary_v1.py .py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 5.3 (Boundary Conditions)
Theorem Support: "Shadow Fixed Points with Dirichlet Boundaries"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    A variant of the basic shadow fixed point experiment using Dirichlet
    Boundary Conditions (Fixed Endpoints).
    
    The script implements a 3-point integer averaging kernel where the
    endpoints are clamped to their original values (D[0]=X[0], D[-1]=X[-1]).
    It iterates the decomposition to verify that the Shadow component
    stabilizes even when the boundaries are strictly constrained.

ADVERSARIAL CONDITIONS:
    - Input:                   Fixed integer sequence [7, 3, 9, 1, 8, 2, 6, 4]
    - Boundary:                Dirichlet (Clamped start/end)
    - Max Levels:              30

PASS CRITERIA:
    1. Convergence:            System detects "SHADOW FIXED POINT REACHED".
    2. Boundary Integrity:     Endpoints remain constant (7 and 4).

USAGE:
    python3 exp_core_val_dirichlet_shadow_fixed_point.py --verbose

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
            D[i] = X[i]  # boundary clamped
        elif i == n - 1:
            D[i] = X[i]  # boundary clamped
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

    left_boundary = X[0]
    right_boundary = X[-1]

    levels = 30

    current = X
    prev_shadow = None

    print("Initial X:")
    print(X)

    for k in range(1, levels + 1):
        D, S = rl_pair(current)

        # enforce boundary
        D[0] = left_boundary
        D[-1] = right_boundary

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
