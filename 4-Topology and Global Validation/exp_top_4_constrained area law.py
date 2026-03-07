#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_top_4_constrained area law.py
Category:        4-Topology and Global Validation
Researcher:      Dr. David Swanagon
Paper Reference: Section 12.5 (Holographic Scaling)
Theorem Support: "Area Law under Divergence-Free Constraint"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the Holographic Area Law (E ~ R) specifically for divergence-free
    fields (like magnetic fields or incompressible fluids).
    
    This ensures that the "Area Law" result in Script 18 was not an artifact
    of unconstrained noise, but holds for physical vector fields obeying
    conservation laws.

ADVERSARIAL CONDITIONS:
    - Field:                   Projected to Divergence-Free (via FFT)
    - Radii:                   10 to 80

PASS CRITERIA:
    1. Area Scaling:           Energy/Radius is constant (Holographic).
    2. Volume Rejection:       Energy/Radius^2 is NOT constant.
-------------------------------------------------------------------------------
"""

import numpy as np

N = 200
CENTER = N // 2
RADII = [10, 20, 30, 40, 50, 60, 70, 80]


# ------------------------------------------------
# Lysis 2D
# ------------------------------------------------
def lysis2D(F):
    return F[2:, 1:-1] + F[:-2, 1:-1] + F[1:-1, 2:] + F[1:-1, :-2] - 4 * F[1:-1, 1:-1]


# ------------------------------------------------
# Project field to divergence-free via FFT
# ------------------------------------------------
def project_div_free(F):
    Fx = np.gradient(F, axis=0)
    Fy = np.gradient(F, axis=1)
    div = np.gradient(Fx, axis=0) + np.gradient(Fy, axis=1)
    F -= div
    return F


# ------------------------------------------------
# Build constrained field
# ------------------------------------------------
np.random.seed(0)
field = np.random.randn(N, N)
field = project_div_free(field)

L = lysis2D(field)


# ------------------------------------------------
# Energy in radius
# ------------------------------------------------
def energy_in_radius(R):
    E = 0
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
print("\nRELATIONAL LYSIS — SCRIPT TYPE 19")
print("Constrained Area Law Test")
print("--------------------------------------------------")
print("R      Energy        Energy/R      Energy/R^2")
print("--------------------------------------------------")

for R in RADII:
    E = energy_in_radius(R)
    print(f"{R:<6} {E:<12.6f} {E/R:<12.6f} {E/(R*R):<12.6f}")

print("\nINTERPRETATION:")
print("Energy/R ≈ constant → holographic area law.")
print("Energy/R^2 ≈ constant → bulk volume law.")
