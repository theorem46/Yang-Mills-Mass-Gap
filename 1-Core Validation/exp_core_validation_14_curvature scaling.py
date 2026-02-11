"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_14_curvature scaling.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Paper Reference: Section 4.1 (Geometric Curvature)
Theorem Support: "Curvature-Dependent Adjacency"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Computes the intrinsic curvature 'kappa' of a state and tests if
    modifying the diamond by 'theta = alpha * kappa' preserves adjacency.
    
    This validates the self-consistency of the curvature definition.

ADVERSARIAL CONDITIONS:
    - Input:                   Mixed sine wave
    - Alpha:                   1.0

PASS CRITERIA:
    1. Stability:              Adjacency remains stable under curvature shift.
-------------------------------------------------------------------------------
"""

import numpy as np

def L(x):
    return x[2:] - 2*x[1:-1] + x[:-2]

def curvature(x):
    return np.mean(np.abs(L(x)))

def adjacency(z):
    return np.mean(np.abs(z[1:] - z[:-1]))

N = 5000
t = np.linspace(0,2*np.pi,N)

# solved state
x = np.sin(17*t) + 0.4*np.sin(53*t)

# compute curvature
kappa = curvature(x)

alpha = 1.0   # simple scale

theta = alpha * kappa

L1 = L(x)
L2 = L(L1)
L1c = L1[1:-1]

D0 = L1c
Dk = L1c + theta * L2

print("kappa:", kappa)
print("theta:", theta)
print("adjacency(D0):", adjacency(D0))
print("adjacency(Dk):", adjacency(Dk))
