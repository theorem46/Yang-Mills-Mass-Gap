#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_15_projector stability.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Paper Reference: Section 3.3 (Projector Classes)
Theorem Support: "Comparison of Projector Families"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Compares two different Diamond Projector families:
    A) Depth-Mix (L1 + theta*L2)
    B) Adjacency-Shift (L1 + phi*Shift(L1))
    
    Verifies that different projection strategies yield distinct but
    valid geometric energies.

ADVERSARIAL CONDITIONS:
    - Mixing:                  0.5 for both families

PASS CRITERIA:
    1. Distinction:            Energies differ (Families are non-degenerate).
-------------------------------------------------------------------------------
"""

import numpy as np


def L(x):
    return x[2:] - 2 * x[1:-1] + x[:-2]


def energy(z):
    return np.dot(z[1:-1], L(z))


def adjacency(z):
    return np.mean(np.abs(z[1:] - z[:-1]))


N = 5000
t = np.linspace(0, 2 * np.pi, N)
x = np.sin(17 * t) + 0.4 * np.sin(53 * t)

L1 = L(x)
L1c = L1[1:-1]
L2 = L(L1)

theta = 0.5
phi = 0.5

# Projector family A (depth-mix)
D_A = L1c + theta * L2

# Projector family B (adjacency-shift)
shift = np.roll(L1c, 1)
D_B = L1c + phi * shift

print("Solved-state energy (same for both):", energy(x))
print("\nDiamond A:")
print("Energy:", energy(D_A))
print("Adjacency:", adjacency(D_A))

print("\nDiamond B:")
print("Energy:", energy(D_B))
print("Adjacency:", adjacency(D_B))
