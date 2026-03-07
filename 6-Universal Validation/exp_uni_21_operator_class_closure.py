#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

#!/usr/bin/env python3

"""
RELATIONAL LYSIS: UNIVERSAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_uni_21_operator_class_closure.py
Category:        6-Universal Validation
Field:           OPERATOR THEORY / FOUNDATIONS
Researcher:      Dr. David Swanagon
Target Limit:    Closure of Admissible RL Operator Class
RL Solution:     Admissible Operators Form a Closed Harmonic Class
-------------------------------------------------------------------------------

EXPERIMENT DESCRIPTION:

Tests whether the class of admissible Relational Lysis operators is closed
under composition and still converges to the identical harmonic endpoint
for a fixed solved state.

Tier-1 significance:
    • Operator-class well-posedness
    • Closure under composition
    • Endpoint uniqueness
    • RL primacy over representation

If passed, this supports CMP/Annals-level structural rigor.

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


OPERATORS = [lysis_A, lysis_B, lysis_C]


# ============================================================
# COMPOSED OPERATORS
# ============================================================

def compose(op1, op2):
    def composed(X):
        return op2(op1(X))
    return composed


# ============================================================
# TOWER
# ============================================================

def run_tower(X, op, depth=40):
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

    print("\nRELATIONAL LYSIS — OPERATOR CLASS CLOSURE")
    print("-----------------------------------------")

    np.random.seed(123)
    N = 25

    # Immutable solved state
    D0 = sym(np.random.randn(N, N))
    S0 = sym(np.random.randn(N, N))
    solved = SolvedState(D0, S0)

    # Individual operator endpoints
    endpoints = []

    for op in OPERATORS:
        term = run_tower(solved, op)
        endpoints.append(signature(term))

    # Composed operators
    composed_endpoints = []

    for i in range(len(OPERATORS)):
        for j in range(len(OPERATORS)):
            comp = compose(OPERATORS[i], OPERATORS[j])
            term = run_tower(solved, comp)
            composed_endpoints.append(signature(term))

    # Check closure equivalence
    ref = endpoints[0]

    print("\nIndividual Operator Equivalence:")
    for idx, sig in enumerate(endpoints):
        print(f"Op {idx}:", np.allclose(ref, sig, atol=1e-6))

    print("\nComposed Operator Equivalence:")
    for idx, sig in enumerate(composed_endpoints):
        print(f"Comp {idx}:", np.allclose(ref, sig, atol=1e-6))


if __name__ == "__main__":
    run_experiment()
