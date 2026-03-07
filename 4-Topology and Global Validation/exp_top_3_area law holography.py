#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_top_3_area law holography.py
Category:        4-Topology and Global Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 12.5 (Solved-State Transitions and Interaction)
Theorem Support: "Transition-Vertex Correspondence / Area Law"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests whether the "Energy" of the Relational Lysis field scales with the
    Area (Surface) rather than the Volume of the region. This behavior is a
    signature of Holography and Confinement (Area Law for Entropy/Action).
    
    Computes Energy(R) for increasing radii and checks the scaling ratio.

ADVERSARIAL CONDITIONS:
    - Radii:                   [10, 20, 30, 40, 50, 60, 70, 80]
    - Field:                   2D Random Field processed by Lysis

PASS CRITERIA:
    1. Area Law:               Energy / Radius is approximately constant.
    2. Volume Law:             Energy / Radius^2 would be constant (Fail).

USAGE:
    python3 exp_top_val_18_area_law_holography.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
import math

N = 200  # Grid size
CENTER = N // 2
RADII = [10, 20, 30, 40, 50, 60, 70, 80]


# ------------------------------------------------
# Relational Lysis (2D Laplacian)
# ------------------------------------------------
def lysis2D(F):
    return F[2:, 1:-1] + F[:-2, 1:-1] + F[1:-1, 2:] + F[1:-1, :-2] - 4 * F[1:-1, 1:-1]


# ------------------------------------------------
# Build random field
# ------------------------------------------------
np.random.seed(0)
field = np.random.randn(N, N)

# ------------------------------------------------
# Compute Lysis Field
# ------------------------------------------------
L = lysis2D(field)


# ------------------------------------------------
# Energy inside radius
# ------------------------------------------------
def energy_in_radius(R):
    E = 0.0
    for i in range(L.shape[0]):
        for j in range(L.shape[1]):
            x = i + 1 - CENTER
            y = j + 1 - CENTER
            if x * x + y * y <= R * R:
                E += L[i, j] ** 2
    return E


# ------------------------------------------------
# Main
# ------------------------------------------------
print("\nRELATIONAL LYSIS — SCRIPT TYPE 18")
print("Area Law / Holographic Scaling Test")
print("--------------------------------------------------")
print("R      Energy        Energy/R      Energy/R^2")
print("--------------------------------------------------")

for R in RADII:
    E = energy_in_radius(R)
    print(f"{R:<6} {E:<12.6f} {E/R:<12.6f} {E/(R*R):<12.6f}")

print("\nINTERPRETATION:")
print("If Energy/R ≈ constant -> Area law.")
print("If Energy/R^2 ≈ constant -> Volume law.")
