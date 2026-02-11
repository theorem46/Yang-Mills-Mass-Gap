"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_13_adjaceny correlation.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Paper Reference: Section 10.4 (Geometric Correlations)
Theorem Support: "Adjacency-Energy Correlation"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Correlates the "Diamond Energy" with the "Adjacency Spacing" (mean difference)
    across the mixing parameter theta.
    
    Tests whether geometric proximity (adjacency) maps to energetic stability.

ADVERSARIAL CONDITIONS:
    - Theta:                   -2.0 to 2.0

PASS CRITERIA:
    1. Correlation:            Energy and Adjacency metrics track each other.
-------------------------------------------------------------------------------
"""

import numpy as np

def L(x):
    return x[2:] - 2*x[1:-1] + x[:-2]

def energy(z):
    return np.dot(z[1:-1], L(z))

def adjacency_spacing(z):
    return np.mean(np.abs(z[1:] - z[:-1]))

N = 5000
t = np.linspace(0,2*np.pi,N)
x = np.sin(17*t) + 0.4*np.sin(53*t)

L1 = L(x)
L2 = L(L1)
L1c = L1[1:-1]

thetas = [-2,-1,-0.5,0,0.5,1,2]

print("theta   energy(D)        adjacency(D)")

for th in thetas:
    D = L1c + th*L2
    print(th, energy(D), adjacency_spacing(D))
