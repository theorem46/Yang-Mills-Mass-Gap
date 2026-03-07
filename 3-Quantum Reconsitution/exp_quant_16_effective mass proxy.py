#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_16_effective mass proxy.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Paper Reference: Theorem 4.3 (Mass Generation)
Theorem Support: "Geometric Definition of Effective Mass"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Defines two distinct diamond types: "Light-like" (EM analogue) and
    "Dark-like" (Gravity analogue) based on mixing parameters.
    
    Calculates an "Effective Mass Proxy" = Energy / Adjacency^2.
    Verifies that different geometric configurations yield distinct mass
    signatures, supporting the geometric origin of mass.

ADVERSARIAL CONDITIONS:
    - Mixing:                  +0.2 (Light) vs -1.5 (Dark)

PASS CRITERIA:
    1. Distinct Masses:        Proxies yield stable, distinct values.
-------------------------------------------------------------------------------
"""

import numpy as np

def L(x):
    return x[2:] - 2*x[1:-1] + x[:-2]

def energy(z):
    return abs(np.dot(z[1:-1], L(z)))

def adjacency(z):
    return np.mean(np.abs(z[1:] - z[:-1]))

N = 5000
t = np.linspace(0, 2*np.pi, N)
x = np.sin(17*t) + 0.4*np.sin(53*t)

L1 = L(x)
L2 = L(L1)
L1c = L1[1:-1]

# Two projectors
D_light = L1c + 0.2 * L2      # EM-like: higher adjacency
D_dark  = L1c - 1.5 * L2      # Gravity-like: higher energy

print("LIGHT-LIKE DIAMOND")
print("Energy:", energy(D_light))
print("Adjacency:", adjacency(D_light))

print("\nDARK-LIKE DIAMOND")
print("Energy:", energy(D_dark))
print("Adjacency:", adjacency(D_dark))

def eff_mass(D):
    return energy(D) / (adjacency(D)**2)

print("\nEffective mass proxy")
print("Light-like:", eff_mass(D_light))
print("Dark-like:", eff_mass(D_dark))
