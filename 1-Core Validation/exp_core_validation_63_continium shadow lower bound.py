"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_63_continium shadow lower bound.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 12.3, Proposition 12.3 (Shadow Dimensional Stability)
Theorem Support: "Lattice-Independence of the Shadow Residual"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the fundamental robustness of the "Shadow" component across scaling 
    dimensions. In many discrete operators, residuals vanish as N increases; 
    Relational Lysis predicts that the Shadow represents an intrinsic 
    geometric "gap" that should remain bounded away from zero.
    
    The script applies a hierarchical Lysis cascade to random symmetric 
    operators across increasing dimensions (128 to 1024). By measuring the 
    norm of the residual $s$ after convergence, the experiment verifies 
    whether the "Shadow" is a discretization artifact or a true topological 
    feature of the manifold. 
    
    A stable lower bound as N grows supports the existence of a persistent 
    Mass Gap in the continuum limit.

ADVERSARIAL CONDITIONS:
    - Dimensions (N):          [128, 256, 512, 1024]
    - Operator Type:           Random Symmetric (GOE-like)
    - Depth/Steps:             8 Levels, 6 Iterations per level
    - Metric:                  $\ell_2$ norm of the final Shadow residual

PASS CRITERIA:
    1. Non-Vanishing Shadow:   Min/Mean shadow magnitude does not trend 
                               toward zero as N increases.
    2. Spectral Separation:    Indicates a permanent separation between 
                               the Alignment Diamond (Kernel) and Shadow (Gap).

USAGE:
    python3 exp_top_val_continuum_shadow_lower_bound.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np

# ============================================================
# RELATIONAL LYSIS — CONTINUUM SHADOW LOWER-BOUND TEST
# Tests whether shadow magnitude stays bounded away from zero
# as dimension N increases.
# ============================================================

DIM_LIST = [128, 256, 512, 1024]
DEPTH = 8
STEPS = 6
TRIALS = 10

np.set_printoptions(precision=6, suppress=True)

# ----------------------------
# Utilities
# ----------------------------


def normalize(x):
    n = np.linalg.norm(x)
    if n == 0:
        return x
    return x / n


def random_symmetric_operator(n):
    A = np.random.randn(n, n)
    return (A + A.T) / 2


# ----------------------------
# Alignment Diamond
# ----------------------------


def alignment_diamond(x):
    x = normalize(x)
    # simple two-axis projection
    u = normalize(x)
    v = normalize(np.roll(x, 1))
    return normalize(u + v)


# ----------------------------
# Shadow
# ----------------------------


def shadow(x, d):
    return x - np.dot(x, d) * d


# ----------------------------
# One Hierarchical Lysis Step
# ----------------------------


def lysis_step(H, x):
    y = H @ x
    d = alignment_diamond(y)
    s = shadow(y, d)
    return normalize(d + s)


# ----------------------------
# Full Hierarchy
# ----------------------------


def hierarchical_lysis(H, x):
    for _ in range(DEPTH):
        for _ in range(STEPS):
            x = lysis_step(H, x)
    return x


# ----------------------------
# Shadow Magnitude After Convergence
# ----------------------------


def final_shadow_magnitude(H, x):
    x = hierarchical_lysis(H, x)
    d = alignment_diamond(x)
    s = shadow(x, d)
    return np.linalg.norm(s)


# ----------------------------
# Main Experiment
# ----------------------------


def run():
    print("\nRELATIONAL LYSIS — CONTINUUM SHADOW LOWER-BOUND TEST")
    print("-----------------------------------------------------")

    for N in DIM_LIST:
        mins = []
        print(f"\nDimension N = {N}")
        for t in range(TRIALS):
            H = random_symmetric_operator(N)
            x0 = normalize(np.random.randn(N))
            s = final_shadow_magnitude(H, x0)
            mins.append(s)
            print(f" Trial {t}: shadow = {s:.6f}")
        print(f" -> Min shadow:  {np.min(mins):.6f}")
        print(f" -> Mean shadow: {np.mean(mins):.6f}")

    print("\nINTERPRETATION:")
    print("If minimum shadow does NOT trend toward 0 as N grows,")
    print("shadow lower bound is lattice-independent.")
    print("This supports true kernel/gap separation.")


# ----------------------------
if __name__ == "__main__":
    run()
