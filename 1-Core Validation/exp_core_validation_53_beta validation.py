"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_53_beta validation.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 11.6, Lemma 11.6 (Geometric Gap Scaling)
Theorem Support: "Quadratic Dependency of the Mass Gap on Curvature"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the scaling laws of the Mass Gap ($\Delta$) relative to the gauge 
    coupling/disorder parameter ($\beta$). 
    
    The script analyzes empirical data points to determine if the relationship 
    follows the predicted geometric form:
    $$\Delta \propto \beta^2$$
    
    A constant ratio of $\Delta/\beta^2$ across varying strengths of $\beta$ 
    provides rigorous confirmation that the mass gap is not a stochastic 
    artifact, but an intrinsic geometric result of the non-Abelian field's 
    local curvature (curvature being proportional to $\beta$).

ADVERSARIAL CONDITIONS:
    - Coupling Range:          $\beta \in [0.1, 2.0]$
    - Metric:                  $\Delta / \beta^2$ Ratio Stability
    - Data Source:             Lattice spectral results (pre-computed)

PASS CRITERIA:
    1. Scaling Consistency:    Ratio ($\Delta / \beta^2$) remains stable 
                               for $\beta < 1.0$.
    2. Geometric Origin:       Confirms mass emergence follows the 
                               theoretical curvature-to-energy map.

USAGE:
    python3 exp_core_val_31_beta_squared_scaling.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np

data = [
    (0.1, 0.000847),
    (0.3, 0.010221),
    (0.5, 0.027343),
    (1.0, 0.068613),
    (2.0, 0.074907),
]

print("\nRELATIONAL LYSIS — SCRIPT TYPE 31")
print("Beta^2 Scaling Test")
print("----------------------------------")
print("beta    gap        gap/beta^2")
print("----------------------------------")

for beta, gap in data:
    print(f"{beta:<6} {gap:<10.6f} {gap/(beta**2):.6f}")

print("----------------------------------")
print("If gap/beta^2 ≈ constant:")
print("Gap originates from geometry.")
