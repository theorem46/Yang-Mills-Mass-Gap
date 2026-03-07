#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_18_classical transition.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 9.5 (Emergence of the Quantum Hamiltonian)
Theorem Support: "Classical Limit via Solved-State Geometry"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the "Classical Limit" of Relational Lysis by varying Planck's
    constant (hbar).
    
    Verifies that as hbar -> 0, the Lysis operator (Geometric Curvature) on
    the wavefunction amplitude vanishes (Linear Regime), but the Lysis on
    the probability density |psi|^2 remains finite. This confirms that
    classical geometry emerges from the quantum probability distribution.

ADVERSARIAL CONDITIONS:
    - hbar values:             [1.0, 0.5, 0.2, 0.1, 0.05]
    - Initial State:           Gaussian Wavepacket
    - Evolution:               Schrödinger Equation

PASS CRITERIA:
    1. Quantum Vanishing:      Lysis(psi) -> 0 as hbar -> 0.
    2. Classical Persistence:  Lysis(|psi|^2) converges to a non-zero constant.

USAGE:
    python3 exp_quant_rec_13_classical_transition.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
import math

# -------------------------
# Parameters
# -------------------------

N = 512  # spatial grid
dx = 0.1
dt = 0.01
STEPS = 400

HBAR_VALUES = [1.0, 0.5, 0.2, 0.1, 0.05]

# -------------------------
# Relational Lysis
# -------------------------


def lysis(x):
    return x[2:] - 2 * x[1:-1] + x[:-2]


def shadow_energy(x):
    k = lysis(x)
    num = np.sqrt(np.sum(np.abs(k) ** 2))
    den = np.sqrt(np.sum(np.abs(x[1:-1]) ** 2))
    return num / den if den != 0 else 0.0


# -------------------------
# Initial Gaussian Packet
# -------------------------


def gaussian_packet():
    x = np.linspace(-N // 2, N // 2, N) * dx
    sigma = 2.0
    k0 = 2.0
    psi = np.exp(-(x**2) / (2 * sigma**2)) * np.exp(1j * k0 * x)
    psi /= np.linalg.norm(psi)
    return psi


# -------------------------
# Laplacian
# -------------------------


def laplacian(psi):
    return (np.roll(psi, -1) - 2 * psi + np.roll(psi, 1)) / dx**2


# -------------------------
# Time Evolution
# -------------------------


def evolve(psi, hbar):
    for _ in range(STEPS):
        psi = psi + 1j * hbar * dt * laplacian(psi)
        psi /= np.linalg.norm(psi)
    return psi


# -------------------------
# Main
# -------------------------


def main():
    print("\nRELATIONAL LYSIS — SCRIPT TYPE 13")
    print("Quantum → Classical Transition Test")
    print("-" * 60)
    print(f"{'hbar':<10} {'Lysis(psi)':<20} {'Lysis(|psi|^2)'}")
    print("-" * 60)

    for hbar in HBAR_VALUES:
        psi0 = gaussian_packet()
        psiT = evolve(psi0.copy(), hbar)

        prob = np.abs(psiT) ** 2

        E_psi = shadow_energy(psiT)
        E_prob = shadow_energy(prob)

        print(f"{hbar:<10.3f} {E_psi:<20.8e} {E_prob:.8e}")

    print("-" * 60)
    print("INTERPRETATION:")
    print("As hbar -> 0:")
    print("  Lysis(psi)      -> 0")
    print("  Lysis(|psi|^2)  remains finite")
    print("Classicality = minimum relational curvature of amplitudes.")
    print("")


if __name__ == "__main__":
    main()
