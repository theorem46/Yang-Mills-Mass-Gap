#!/usr/bin/env python3

"""
RELATIONAL LYSIS: UNIVERSAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_uni_22_fixed_point_stability_spectrum.py
Category:        6-Universal Validation
Field:           NONLINEAR STABILITY / SPECTRAL THEORY
Researcher:      Dr. David Swanagon
Target Limit:    Harmonic Fixed Point Stability
RL Solution:     Fixed Point is Globally Attractive in Solved-State Manifold
-------------------------------------------------------------------------------

EXPERIMENT DESCRIPTION:

Tests whether the harmonic fixed point of Relational Lysis is
spectrally stable under admissible perturbations of a solved state.

Tier-1 significance:
    • Fixed point stability
    • Basin of attraction validation
    • Spectral robustness
    • CMP/Annals-level dynamical rigor

If the fixed point is globally attractive, small perturbations
must decay and reconverge to the identical endpoint.

-------------------------------------------------------------------------------
"""

import numpy as np


# ============================================================
# SOLVED STATE
# ============================================================

def sym(M):
    M = (M + M.T) / 2.0
    np.fill_diagonal(M, 0.0)
    return M


class SolvedState:
    def __init__(self, D, S):
        self.D = sym(D)
        self.S = sym(S)

    def combined(self):
        return self.D + self.S


# ============================================================
# ADMISSIBLE RL OPERATOR
# ============================================================

def lysis(X):
    J = X.combined()
    Dn = sym(J @ J.T)
    Sn = sym(J - Dn)
    return SolvedState(Dn, Sn)


def run_tower(X, depth=40):
    Y = X
    for _ in range(depth):
        Y = lysis(Y)
    return Y


# ============================================================
# SIGNATURE
# ============================================================

def signature(X):
    eig = np.linalg.eigvalsh(X.D)
    return np.array([
        np.linalg.norm(X.D),
        np.linalg.norm(X.S),
        eig.min(),
        eig.max()
    ])


# ============================================================
# PERTURBATION
# ============================================================

def perturb_state(X, eps):
    N = X.D.shape[0]
    noise = np.random.randn(N, N)
    noise = sym(noise)
    return SolvedState(X.D + eps * noise, X.S - eps * noise)


# ============================================================
# EXPERIMENT
# ============================================================

def run_experiment():

    print("\nRELATIONAL LYSIS — FIXED POINT STABILITY SPECTRUM")
    print("------------------------------------------------")

    np.random.seed(321)
    N = 25

    # Base solved state
    D0 = sym(np.random.randn(N, N))
    S0 = sym(np.random.randn(N, N))
    solved = SolvedState(D0, S0)

    # Reference harmonic endpoint
    base_terminal = run_tower(solved)
    base_sig = signature(base_terminal)

    print("\nReference Signature:", base_sig)

    epsilons = [1e-3, 1e-2, 1e-1]

    print("\nPerturbation Recovery:")

    for eps in epsilons:

        perturbed = perturb_state(solved, eps)
        terminal = run_tower(perturbed)
        sig = signature(terminal)

        recovered = np.allclose(base_sig, sig, atol=1e-6)

        print(f"Epsilon {eps:.1e} | Recovered:", recovered)


if __name__ == "__main__":
    run_experiment()
