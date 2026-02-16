"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_stress_6_curvature saturation.py
Category:        7-Stress Tests
Researcher:      Dr. David Swanagon
Original Date:   February 14, 2026
Paper Reference: (Universal Curvature Bound and Core Regularization)
Theorem Support: "Finite Curvature Saturation in Relational Black Hole Interiors"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Compares the classical Schwarzschild curvature divergence to the
    Relational Lysis (RL) saturated curvature model near r → 0.

    The Kretschmann scalar for Schwarzschild spacetime is:

        K_classical = 48 M^2 / r^6

    which diverges as r → 0, signaling a curvature singularity.

    RL introduces a relational core radius:

        r_min = α M^(1/3)

    which regularizes the invariant:

        K_RL = 48 M^2 / (r^6 + r_min^6)

    The script evaluates both invariants across decreasing radii,
    including r = 0, to demonstrate:

        • Classical divergence (K → ∞)
        • RL curvature saturation (finite maximum)

    This directly tests the Universal Curvature Bound hypothesis.

ADVERSARIAL CONDITIONS:
    - Geometry:                Schwarzschild vs RL-Regularized
    - Black Hole Mass:         M = 10 (geometric units)
    - Core Scaling:            r_min = α M^(1/3)
    - Alpha:                   0.05
    - Radial Sweep:            r = 10 → 0
    - Singularity Probe:       Explicit r = 0 evaluation

PASS CRITERIA:
    1. Classical Divergence:   K_classical → ∞ at r = 0.
    2. RL Saturation:          K_RL remains finite at r = 0.
    3. Ratio Collapse:         K_RL / K_classical → 0 as r → 0.

USAGE:
    python3 exp_bh_step1_curvature_saturation.py

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""


import numpy as np

def run_experiment():
    print("\nRELATIONAL LYSIS: BLACK HOLE STEP 1")
    print("Curvature Saturation vs. Classical Divergence")
    print("------------------------------------------------------------")
    print(f"{'Radius (r)':<12} | {'Classical K':<15} | {'RL K (Saturated)':<15} | {'Ratio'}")
    print("-" * 65)

    # Parameters
    M = 10.0            # Black Hole Mass
    alpha = 0.05        # Scaling parameter
    r_min = alpha * (M**(1.0/3.0)) # Relational Core Radius
    
    # We probe from outside the horizon down to r=0
    # Standard Kretschmann Scalar for Schwarzschild: K = 48 M^2 / r^6
    
    radii = [10.0, 5.0, 2.0, 1.0, 0.5, 0.1, 0.01, 0.0]

    for r in radii:
        # Classical Singularity
        if r == 0:
            K_classical = float('inf')
        else:
            K_classical = (48 * M**2) / (r**6)

        # Relational Lysis Saturated Curvature
        # The core r_min acts as a regulator in the denominator
        # K_rl = 48 M^2 / (r^6 + r_min^6)
        K_rl = (48 * M**2) / (r**6 + r_min**6)

        # Output formatting
        if r == 0:
            ratio = 0.0
            print(f"{r:<12.2f} | {'INF':<15} | {K_rl:<15.4e} | {ratio:.4f}")
        else:
            ratio = K_rl / K_classical
            print(f"{r:<12.2f} | {K_rl:<15.4e} | {K_rl:<15.4e} | {ratio:.4f}")

    print("-" * 65)
    print("INTERPRETATION:")
    print(f"Classical curvature explodes at r=0. RL curvature saturates at {K_rl:.4e}.")
    print("This finite maximum is the 'Universal Curvature Bound'.")

if __name__ == "__main__":
    run_experiment()