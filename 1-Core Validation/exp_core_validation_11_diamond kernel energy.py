#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_11_diamond kernel energy.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Paper Reference: Definition 3.1 (Solved State)
Theorem Support: "Separation of State Energy and Diamond Energy"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Compares the energy of the raw state E(x) vs the energy of its
    extracted Diamond E(D).
    
    Demonstrates that E(D) << E(x), confirming that the Diamond represents
    the "Kernel" or "Harmonic Backbone" of the state, while the energy
    resides primarily in the Shadow.

ADVERSARIAL CONDITIONS:
    - Frequencies:             m = 2 to 64

PASS CRITERIA:
    1. Separation:             E(D) is orders of magnitude smaller than E(x).
-------------------------------------------------------------------------------
"""

import numpy as np


def L(x):
    return x[2:] - 2 * x[1:-1] + x[:-2]


def energy(x):
    return np.dot(x[1:-1], L(x))


def diamond_energy(x):
    Dx = L(x)
    return np.dot(Dx[1:-1], L(Dx))


# build family of solved states
N = 4000
t = np.linspace(0, 2 * np.pi, N)

ms = [2, 4, 8, 16, 32, 64]

results = []

for m in ms:
    x = np.sin(m * t)
    Ex = energy(x)
    ED = diamond_energy(x)
    results.append((m, Ex, ED))

for m, Ex, ED in results:
    print(f"m={m:3d}  E(x)={Ex:.6e}   E(D)={ED:.6e}")
