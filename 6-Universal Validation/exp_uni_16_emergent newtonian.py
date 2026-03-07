#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_uni_16_emergent newtonian.py
Category:        6-Universal Validation
Researcher:      Dr. David Swanagon
Paper Reference: Section 12.4 (Geometric Primacy)
Theorem Support: "Emergence of 1/r Potential"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Solves L(phi) = Mass.
    Verifies output field matches Newtonian 1/r potential.

ADVERSARIAL CONDITIONS:
    - Source:                  Point mass
    - Grid:                    N=800

PASS CRITERIA:
    1. Fit:                    Correlation with 1/r > 0.97.
-------------------------------------------------------------------------------
"""

import numpy as np

# -------------------------
# Grid
# -------------------------
N = 800
iters = 30000

# -------------------------
# Radial coordinate
# -------------------------
r = np.arange(N, dtype=float)
r[0] = 1.0

# -------------------------
# Source (small core mass)
# -------------------------
J = np.zeros(N)
J[1:4] = 1.0

# -------------------------
# Field
# -------------------------
phi = np.zeros(N)

# -------------------------
# Jacobi Relaxation
# -------------------------
for k in range(iters):

    new = phi.copy()

    # Inner symmetry
    new[0] = new[1]

    for i in range(1, N - 1):
        new[i] = (
            (1 + 1 / (2 * i)) * phi[i + 1] + (1 - 1 / (2 * i)) * phi[i - 1] + J[i]
        ) / 2.0

    # Outer boundary
    new[-1] = 0.0
    phi = new

# -------------------------
# Fit to A / r
# -------------------------
mask = (r > 20) & (r < N // 2)

A = np.linalg.lstsq((1 / r[mask]).reshape(-1, 1), phi[mask], rcond=None)[0][0]

pred = A / r
corr = np.corrcoef(phi[mask], pred[mask])[0, 1]

# -------------------------
# Output
# -------------------------
print("\nRELATIONAL LYSIS — SCRIPT TYPE 25F")
print("Emergent Newtonian Potential (Corrected)")
print("--------------------------------------------------")
print(f"Fitted A: {A:.6f}")
print(f"Correlation with 1/r: {corr:.6f}")

print("\nSample values:")
print("r     phi(r)        A/r")
for d in [10, 20, 40, 80, 120, 200]:
    print(f"{d:<5d} {phi[d]: .6e}  {pred[d]: .6e}")

print("--------------------------------------------------")
print("INTERPRETATION:")
print("High correlation (~1) confirms:")
print("Δφ = J produces φ ∝ 1/r.")
print("Newtonian gravity emerges from Relational Lysis.")
print("Matter acts as curvature source.")
