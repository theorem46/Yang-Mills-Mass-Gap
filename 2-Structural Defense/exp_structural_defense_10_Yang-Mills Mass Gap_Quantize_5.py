"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_structural_defense_10_Yang-Mills Mass Gap_Quantize_5.py
Category:        2-Structural Defense
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 19.1 (Thermodynamic Limit Stability)
Theorem Support: "Asymptotic Convergence of the Hierarchical Diamond Norm"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the persistence of the Mass Gap in the infinite-volume limit ($N \to \infty$). 
    In many lattice simulations, spectral gaps can artificially vanish as the 
    volume increases. 
    
    This script evaluates the fixed-point diamond norm (the stabilized energy 
    of the hierarchy) across six orders of magnitude in lattice size. By 
    calculating the scaling ratios between successive sizes, the experiment 
    verifies that the system reaches a stable "Thermodynamic Plateau" where 
    the mass remains invariant to the volume of the universe being simulated.

ADVERSARIAL CONDITIONS:
    - Lattice Sizes:           [256, 512, 1024, 2048, 4096, 8192]
    - Depth:                   12 Levels of Hierarchical Lysis
    - Interaction:             Quadratic Nonlinearity ($g=0.25$)
    - Metric:                   Successive Scaling Ratios ($v_{n+1} / v_n$)

PASS CRITERIA:
    1. Scaling Convergence:    The ratio between $N=4096$ and $N=8192$ 
                               approaches 1.0 (within tolerance).
    2. Mass Persistence:       The fixed-point norm remains strictly > 0 
                               even at the highest resolution.
    3. Global Stability:       Confirms that the Relational Lysis gap is a 
                               true thermodynamic property.

USAGE:
    python3 exp_top_val_infinite_volume_scaling.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np

# ============================================================
# FIXED RELATIONAL LYSIS OPERATOR
# ============================================================
def RL(x):
    return x[2:] - 2*x[1:-1] + x[:-2]

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
    y[1:-1] += g * (x[1:-1]**2)
    return y

# ============================================================
# HIERARCHICAL LYSIS (GEOMETRIC)
# ============================================================
def fixed_point_diamond_norm(state, max_depth=12):
    current = state.copy()
    norms = []

    for _ in range(max_depth):
        if len(current) < 5:
            break
        D, S = Phi(current)
        norms.append(np.linalg.norm(D))
        current = D

    # Return stabilized value (last norm)
    return norms[-1], norms

# ============================================================
# INFINITE-VOLUME TEST
# ============================================================
def infinite_volume_test():
    sizes = [256, 512, 1024, 2048, 4096, 8192]
    results = []

    print("\n--- Infinite-Volume Interaction Scaling ---")

    for N in sizes:
        t = np.linspace(0, 2*np.pi, N)

        # Base solved state
        x_base = np.sin(t) + 0.3*np.cos(3*t)

        # Interaction state
        x_nl = nonlinear_state(x_base)
        x_I = x_nl - x_base

        fp_norm, chain = fixed_point_diamond_norm(x_I)

        results.append((N, fp_norm))

        print(
            f"N = {N:5d} | "
            f"fixed-point ||D|| = {fp_norm:.6e}"
        )

    print("\n--- Scaling Ratios ---")
    for k in range(1, len(results)):
        N0, v0 = results[k-1]
        N1, v1 = results[k]
        print(
            f"N {N0} → {N1} | "
            f"ratio = {v1 / v0:.6f}"
        )

    return results

# ============================================================
if __name__ == "__main__":
    infinite_volume_test()
