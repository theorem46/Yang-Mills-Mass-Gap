#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_19_entanglement geometry.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 10.2 (Geometric Entanglement Entropy)
Theorem Support: "Entanglement as Relational Curvature"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the hypothesis that quantum entanglement manifests as geometric
    curvature (roughness) in the density matrix state space.
    
    Calculates the Lysis Energy of Product, Separable, and Entangled states.
    If Entangled > Separable > Product, it confirms that correlation adds
    geometric "stress" to the manifold.

ADVERSARIAL CONDITIONS:
    - State Types:             Product (|00>), Separable (|00>+|11>), Entangled (Bell)
    - Representation:          Density Matrix (rho)

PASS CRITERIA:
    1. Hierarchy:              Energy(Entangled) > Energy(Separable) > Energy(Product).

USAGE:
    python3 exp_quant_rec_14_entanglement_geometry.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
import math

# -------------------------------
# Relational Lysis
# -------------------------------


def lysis(x):
    return np.array([x[i + 2] - 2 * x[i + 1] + x[i] for i in range(len(x) - 2)])


def energy(x):
    Lx = lysis(x)
    return math.sqrt(np.sum(Lx**2))


# -------------------------------
# Normalize
# -------------------------------


def normalize(v):
    return v / np.linalg.norm(v)


# -------------------------------
# Build Density Matrix
# -------------------------------


def density_matrix(psi):
    return np.outer(psi, psi.conjugate())


# -------------------------------
# Flatten Density Matrix
# -------------------------------


def flatten_dm(rho):
    seq = []
    for row in rho:
        for val in row:
            seq.append(val.real)
    return np.array(seq)


# -------------------------------
# States
# -------------------------------

psi_product = np.array([1, 0, 0, 0], dtype=float)

psi_sep = normalize(np.array([1, 1, 0, 0], dtype=float))

psi_ent = normalize(np.array([1, 0, 0, 1], dtype=float))

# -------------------------------
# Main
# -------------------------------


def main():
    print("\nRELATIONAL LYSIS — SCRIPT TYPE 14B")
    print("Entanglement Geometry (Density Matrix)")
    print("-" * 60)

    rho_prod = density_matrix(psi_product)
    rho_sep = density_matrix(psi_sep)
    rho_ent = density_matrix(psi_ent)

    E_prod = energy(flatten_dm(rho_prod))
    E_sep = energy(flatten_dm(rho_sep))
    E_ent = energy(flatten_dm(rho_ent))

    print(f"Product State Energy:    {E_prod:.12e}")
    print(f"Separable State Energy:  {E_sep:.12e}")
    print(f"Entangled State Energy:  {E_ent:.12e}")

    print("\nRatios:")
    print(f"Sep / Prod = {E_sep/E_prod:.6f}")
    print(f"Ent / Sep  = {E_ent/E_sep:.6f}")

    print("\nINTERPRETATION:")
    print("If Entangled > Separable > Product:")
    print("Entanglement has geometric curvature signature.")


if __name__ == "__main__":
    main()
