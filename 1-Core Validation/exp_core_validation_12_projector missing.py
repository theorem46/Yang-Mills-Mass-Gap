"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_12_projector missing.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Paper Reference: Section 3.3 (Operator Composition)
Theorem Support: "Stability of Projector Mixing"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Investigates the stability of the Diamond Energy under a mixed projection
    operator D = L1 + theta * L2 (first and second order Lysis).
    
    Verifies that the energy varies smoothly with the mixing parameter theta,
    indicating a well-behaved operator manifold.

ADVERSARIAL CONDITIONS:
    - Theta:                   -2.0 to 2.0
    - Input:                   Mixed sine wave

PASS CRITERIA:
    1. Continuity:             Energy values change smoothly without singularities.
-------------------------------------------------------------------------------
"""

import numpy as np

def L(x):
    return x[2:] - 2*x[1:-1] + x[:-2]

def energy(z):
    return np.dot(z[1:-1], L(z))

N = 5000
t = np.linspace(0,2*np.pi,N)
x = np.sin(17*t) + 0.4*np.sin(53*t)

L1 = L(x)
L2 = L(L1)

L1c = L1[1:-1]   # align geometry

thetas = [-2,-1,-0.5,0,0.5,1,2]

print("theta   diamond_energy")

for th in thetas:
    D = L1c + th*L2
    print(th, energy(D))
