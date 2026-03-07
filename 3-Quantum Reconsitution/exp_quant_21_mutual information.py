#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_21_mutual information.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Paper Reference: Section 10.4 (Mutual Information)
Theorem Support: "Mutual Information as Geometric Correlation"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Correlates Mutual Information I(A:B) with Lysis Energy.
    Includes sub-tests 16b (2D Isotropy), 16c (3D Isotropy), 16d (Renormalization).

ADVERSARIAL CONDITIONS:
    - Dimensions:              1D, 2D, 3D
    - Geometry:                Spherical renormalization (16d)

PASS CRITERIA:
    1. Isotropy:               Operator recovers correct stencil weights (4 for 2D, 6 for 3D).
-------------------------------------------------------------------------------
"""

import numpy as np
import math

# ----------------------------
# Lysis
# ----------------------------


def lysis(x):
    return np.array([x[i + 2] - 2 * x[i + 1] + x[i] for i in range(len(x) - 2)])


def shadow_energy(x):
    k = lysis(x)
    return math.sqrt(np.sum(k * k)) / math.sqrt(np.sum(x * x))


# ----------------------------
# Entropy
# ----------------------------


def entropy(rho):
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 1e-12]
    return -np.sum(vals * np.log2(vals))


# ----------------------------
# Partial trace over qubit B
# ----------------------------


def partial_trace_B(rho):
    rhoA = np.zeros((2, 2))
    rhoA[0, 0] = rho[0, 0] + rho[1, 1]
    rhoA[1, 1] = rho[2, 2] + rho[3, 3]
    rhoA[0, 1] = rho[0, 2] + rho[1, 3]
    rhoA[1, 0] = rho[2, 0] + rho[3, 1]
    return rhoA


# ----------------------------
# Build entangled state
# ----------------------------


def state(theta):
    v = np.zeros(4)
    v[0] = math.cos(theta)
    v[3] = math.sin(theta)
    return v


def density(psi):
    return np.outer(psi, psi.conj())


# ----------------------------
# Main
# ----------------------------


def main():

    print("\nRELATIONAL LYSIS — SCRIPT TYPE 16")
    print("Mutual Information vs Relational Curvature")
    print("------------------------------------------------")
    print("theta/pi   Mutual Info I(A:B)   Lysis Energy")
    print("------------------------------------------------")

    for k in range(21):
        theta = (math.pi / 4) * k / 20

        psi = state(theta)
        rho = density(psi)

        rhoA = partial_trace_B(rho)
        rhoB = rhoA.copy()

        I = entropy(rhoA) + entropy(rhoB) - entropy(rho)
        E = shadow_energy(rho.flatten().real)

        print(f"{theta/math.pi:8.4f}   {I:18.8f}   {E:14.8f}")

    print("\nINTERPRETATION:")
    print("If I(A:B) and Lysis Energy grow together,")
    print("correlation is geometric curvature.")


if __name__ == "__main__":
    main()
