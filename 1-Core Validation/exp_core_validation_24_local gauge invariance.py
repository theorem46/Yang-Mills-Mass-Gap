#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_24_local gauge invariance.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 3.1, Definition 3.3 (Reconstruction Invariance)
Theorem Support: "Reconstruction Invariance under Gauge Transformations"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Validates that the Relational Lysis Energy is invariant under random local
    gauge transformations G(x).
    
    E(psi, U) should equal E(G*psi, G*U*G^dag). This confirms that the
    "Shadow Energy" is a physical observable (Gauge Invariant quantity).

ADVERSARIAL CONDITIONS:
    - Lattice:                 N = 3000
    - Transformations:         Randomized Phase at every site (High entropy)

PASS CRITERIA:
    1. Invariance Ratio:       E_transformed / E_original == 1.0 (within precision)

USAGE:
    python3 exp_core_val_06_local_gauge_invariance.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
import math

np.random.seed(1)

N = 3000

# ------------------------------------------------
# Helpers
# ------------------------------------------------


def random_phase():
    return np.exp(1j * 2 * math.pi * np.random.rand())


# ------------------------------------------------
# Build Fields
# ------------------------------------------------


def build_scalar_field():
    return [random_phase() for _ in range(N)]


def build_gauge_field():
    # Links live between sites → N-1
    return [random_phase() for _ in range(N - 1)]


# ------------------------------------------------
# Gauge-Covariant Lysis
# ------------------------------------------------


def gauge_lysis(psi, U):
    out = []
    for i in range(1, N - 1):
        val = U[i] * psi[i + 1] - 2 * psi[i] + np.conj(U[i - 1]) * psi[i - 1]
        out.append(val)
    return np.array(out)


def energy(vec):
    return np.sum(np.abs(vec) ** 2)


# ------------------------------------------------
# Local Gauge Transform
# ------------------------------------------------


def gauge_transform(psi, U):
    G = [random_phase() for _ in range(N)]

    psi2 = [G[i] * psi[i] for i in range(N)]

    U2 = []
    for i in range(N - 1):
        U2.append(G[i] * U[i] * np.conj(G[i + 1]))

    return psi2, U2


# ------------------------------------------------
# Main
# ------------------------------------------------


def main():
    print("\nRELATIONAL LYSIS — SCRIPT TYPE 6")
    print("Local Gauge Invariance Test")
    print("-" * 50)

    psi = build_scalar_field()
    U = build_gauge_field()

    L1 = gauge_lysis(psi, U)
    E1 = energy(L1)

    psi2, U2 = gauge_transform(psi, U)
    L2 = gauge_lysis(psi2, U2)
    E2 = energy(L2)

    print("Original Energy:     ", E1)
    print("Gauge Rotated Energy:", E2)
    print("Ratio:               ", E2 / E1)

    print("\nINTERPRETATION:")
    print("Ratio ≈ 1 confirms:")
    print("Relational Lysis is locally gauge invariant.")


if __name__ == "__main__":
    main()
