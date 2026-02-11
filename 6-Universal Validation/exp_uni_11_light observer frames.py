"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_uni_11_light observer frames.py
Category:        6-Universal Validation
Researcher:      Dr. David Swanagon
Paper Reference: Section 12.1 (Emergent Metric)
Theorem Support: "Observer-Dependent Geometric Measurements"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Simulates two "Observers" residing in different curvature environments
    (Flat vs Curved), represented by different mixing parameters `theta`.
    
    Compares the Energy and Adjacency measurements reported by each observer
    for the same underlying state. This validates the relativistic consistency
    of the Relational Lysis framework.

ADVERSARIAL CONDITIONS:
    - Flat Observer:           Theta = 0.001
    - Curved Observer:         Theta = 0.8

PASS CRITERIA:
    1. Relationality:          Measurements differ systematically based on frame.
-------------------------------------------------------------------------------
"""

import numpy as np


def L(x):
    return x[2:] - 2 * x[1:-1] + x[:-2]


def energy(z):
    return abs(np.dot(z[1:-1], L(z)))


def adjacency(z):
    return np.mean(np.abs(z[1:] - z[:-1]))


# solved state
N = 5000
t = np.linspace(0, 2 * np.pi, N)
x = np.sin(17 * t) + 0.4 * np.sin(53 * t)

L1 = L(x)
L2 = L(L1)
L1c = L1[1:-1]

# two observers (different curvature environments)
theta_flat = 0.001  # weak curvature observer
theta_curv = 0.8  # strong curvature observer

D_flat = L1c + theta_flat * L2
D_curv = L1c + theta_curv * L2

print("FLAT OBSERVER")
print("Energy:", energy(D_flat))
print("Adjacency:", adjacency(D_flat))

print("\nCURVED OBSERVER")
print("Energy:", energy(D_curv))
print("Adjacency:", adjacency(D_curv))
