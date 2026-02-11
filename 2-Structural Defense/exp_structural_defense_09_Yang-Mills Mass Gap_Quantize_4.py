"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_structural_defense_09_Yang-Mills Mass Gap_Quantize_4.py
Category:        2-Structural Defense
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 20.2 (The Interaction Convergence Axiom)
Theorem Support: "Hierarchical Admissibility of Nonlinear Gauge Potentials"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the "Admissibility" of nonlinear interactions within the Relational 
    Lysis hierarchy. The script evaluates whether the energy resulting from 
    a quadratic interaction ($x^2$) can be decomposed into a stable tower of 
    Alignment Diamonds and Shadows. 
    
    By monitoring two specific metrics—Monotone Shadow Decay and Geometric 
    Diamond Convergence—the script determines if the interaction term 
    possesses the "Relational DNA" required to be considered a physical 
    solved state. Failure to converge would indicate that the interaction 
    is non-physical or breaks the continuum structure of the theory.

ADVERSARIAL CONDITIONS:
    - Lattice Size:             2048 (High-resolution field)
    - Interaction Type:         Quadratic Nonlinearity ($g=0.25$)
    - Hierarchical Depth:       12 Levels
    - Stability Metric:         Standard Deviation of the last three energy 
                                ratios ($\sigma < 1e-3$).

PASS CRITERIA:
    1. Shadow Monotonicity:    ||S|| must not increase across hierarchical 
                               levels (within numerical tolerance).
    2. Geometric Stability:    Energy ratios ($||D_{k+1}||/||D_k||$) must 
                               stabilize, indicating a fixed-point attractor.
    3. Structural Admissibility: Confirms that nonlinearities are "tamed" by 
                               the Lysis hierarchy.

USAGE:
    python3 exp_int_mech_interaction_solved_state_diagnostic.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np


# ============================================================
# FIXED RELATIONAL LYSIS OPERATOR (DO NOT MODIFY)
# ============================================================
def RL(x):
    return x[2:] - 2 * x[1:-1] + x[:-2]


# ============================================================
# SOLVED-STATE DECOMPOSITION
# ============================================================
def Phi(x):
    D = RL(x)
    S = x[1:-1] - D
    return D, S


# ============================================================
# NON-LINEAR INTERACTION STATE
# ============================================================
def nonlinear_state(x, g=0.25):
    y = x.copy()
    y[1:-1] += g * (x[1:-1] ** 2)
    return y


# ============================================================
# HIERARCHICAL LYSIS (RL-CORRECT)
# ============================================================
def hierarchical_lysis(state, max_depth=12):
    diamonds = []
    shadows = []
    norms = []

    current = state.copy()
    for level in range(max_depth):
        if len(current) < 5:
            break

        D, S = Phi(current)
        diamonds.append(D)
        shadows.append(S)
        norms.append(np.linalg.norm(D))

        current = D

    return diamonds, shadows, norms


# ============================================================
# MAIN TEST
# ============================================================
def test_interaction_as_solved_state():
    N = 2048
    t = np.linspace(0, 2 * np.pi, N)

    x_base = np.sin(t) + 0.3 * np.cos(3 * t)
    x_nl = nonlinear_state(x_base)
    x_interaction = x_nl - x_base

    D_chain, S_chain, D_norms = hierarchical_lysis(x_interaction)

    print("\n--- Interaction Solved-State Diagnostics ---")
    for k in range(len(D_chain)):
        print(
            f"Level {k}: "
            f"||D|| = {D_norms[k]:.6e}, "
            f"||S|| = {np.linalg.norm(S_chain[k]):.6e}, "
            f"ratio = {D_norms[k]/D_norms[k-1]:.6f}"
            if k > 0
            else ""
        )

    # ----------------------------------------
    # RL-ADMISSIBLE VERDICTS
    # ----------------------------------------

    # Shadow decay (residual only)
    shadow_decay = all(
        np.linalg.norm(S_chain[k + 1]) <= np.linalg.norm(S_chain[k]) + 1e-10
        for k in range(len(S_chain) - 1)
    )

    # Geometric convergence: norm ratios stabilize
    ratios = [
        D_norms[k + 1] / D_norms[k] for k in range(len(D_norms) - 1) if D_norms[k] > 0
    ]

    ratio_converges = len(ratios) > 3 and np.std(ratios[-3:]) < 1e-3

    print("\n--- Verdict ---")
    print("Shadow monotone decay:", shadow_decay)
    print("Diamond geometric convergence:", ratio_converges)

    if shadow_decay and ratio_converges:
        print("\nPASS: Interaction is a genuine hierarchical solved state.")
    else:
        print("\nFAIL: Interaction does not converge geometrically.")


# ============================================================
if __name__ == "__main__":
    test_interaction_as_solved_state()
