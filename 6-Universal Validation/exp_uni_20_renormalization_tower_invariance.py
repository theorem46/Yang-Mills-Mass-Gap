#!/usr/bin/env python3

"""
RELATIONAL LYSIS: UNIVERSAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_uni_20_renormalization_tower_invariance.py
Category:        6-Universal Validation
Field:           FIELD THEORY / RENORMALIZATION
Researcher:      Dr. David Swanagon
Target Limit:    Renormalization Consistency
RL Solution:     Operator-Admissible Depth Invariance on Identical Solved State
-------------------------------------------------------------------------------

DESIGN:

This experiment tests renormalization invariance correctly by:

1. Using ONE identical solved state (immutable once in tower)
2. Applying MULTIPLE admissible RL operators (same axioms)
3. Varying hierarchical depth
4. Verifying convergence to identical harmonic endpoint

This matches CMP-level requirements:
    • Operator admissibility class
    • Fixed point uniqueness
    • Depth invariance
    • Representation independence
-------------------------------------------------------------------------------
"""

import numpy as np


# ============================================================
# SOLVED STATE STRUCTURE
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
# ADMISSIBLE RL OPERATORS
# ============================================================

def lysis_A(X):
    J = X.combined()
    Dn = sym(J @ J.T)
    Sn = sym(J - Dn)
    return SolvedState(Dn, Sn)


def lysis_B(X):
    J = X.combined()
    Dn = sym(J.T @ J)
    Sn = sym(J - Dn)
    return SolvedState(Dn, Sn)


def lysis_C(X):
    J = X.combined()
    Dn = sym(J @ J)
    Sn = sym(J - Dn)
    return SolvedState(Dn, Sn)


OPERATORS = {
    "A": lysis_A,
    "B": lysis_B,
    "C": lysis_C
}


# ============================================================
# TOWER
# ============================================================

def run_tower(X, op, depth):
    Y = X
    for _ in range(depth):
        Y = op(Y)
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
# EXPERIMENT
# ============================================================

def run_experiment():

    print("\nRELATIONAL LYSIS — RENORMALIZATION TOWER INVARIANCE (CMP v2)")
    print("-------------------------------------------------------------")

    np.random.seed(42)
    N = 25

    # ONE immutable solved state
    D0 = sym(np.random.randn(N, N))
    S0 = sym(np.random.randn(N, N))
    solved = SolvedState(D0, S0)

    depths = [10, 30, 80]

    results = {}

    for name, op in OPERATORS.items():

        print(f"\nOperator {name}")

        op_results = []

        for d in depths:

            terminal = run_tower(solved, op, d)
            sig = signature(terminal)

            op_results.append(sig)

            print(f"Depth {d:3d} | Signature {sig}")

        # Depth invariance check
        base = op_results[-1]
        invariant = all(np.allclose(base, s, atol=1e-6) for s in op_results)

        print("Depth Invariance:", invariant)

        results[name] = base

    # Operator invariance check
    print("\nOperator Endpoint Equivalence:")

    ref = results["A"]

    for name in results:
        print(f"A vs {name}:", np.allclose(ref, results[name], atol=1e-6))


if __name__ == "__main__":
    run_experiment()
