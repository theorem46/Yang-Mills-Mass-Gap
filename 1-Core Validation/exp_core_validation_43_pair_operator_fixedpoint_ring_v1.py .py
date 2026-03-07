#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_43_pair_operator_fixedpoint_ring_v1.py .py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 3.7 (Hierarchical Lysis)
Theorem Support: "Shadow Fixed Points on Periodic Lattices"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    A variant of the basic shadow fixed point experiment using Periodic
    Boundary Conditions (Ring Topology).
    
    The script implements a 3-point integer averaging kernel with wrap-around
    indexing. It iterates the decomposition to verify that the Shadow component
    stabilizes, confirming attractor dynamics on closed loops (toroidal topology).

ADVERSARIAL CONDITIONS:
    - Input:                   Fixed integer sequence [7, 3, 9, 1, 8, 2, 6, 4]
    - Topology:                Periodic (Ring)
    - Max Levels:              40

PASS CRITERIA:
    1. Convergence:            System detects "SHADOW FIXED POINT REACHED".
    2. Stability:              Shadow trace remains invariant between levels.

USAGE:
    python3 exp_core_val_periodic_shadow_fixed_point.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

def alignment_diamond(X):
    n = len(X)
    D = [0] * n
    for i in range(n):
        left = X[(i - 1) % n]
        right = X[(i + 1) % n]
        D[i] = (left + X[i] + right) // 3
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

    levels = 40

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
