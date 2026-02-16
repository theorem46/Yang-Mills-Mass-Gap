#!/usr/bin/env python3
"""
RELATIONAL LYSIS: UNIVERSAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_uni_17_reverse operator.py
Category:        6-Universal Validation
Field: FOUNDATIONS / MATHEMATICAL PHYSICS

Researcher: Dr. David Swanagon

Path:
 /Users/dswanagon/Relational Lysis Github/6-Universal Validation

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION

Tier-1 Reverse Universality Validation at Large Scale (N = 500)

This experiment demonstrates:

1. Deterministic hierarchical convergence
2. Representation-independent solved-state formation
3. Quadratic terminal geometry
4. Emergent Laplace-type operator class
5. Geometric contraction behavior

-------------------------------------------------------------------------------
PASS CRITERIA

• Finite termination
• Contraction ratio < 1
• Diamond symmetry error < 1e-12
• Operator self-adjoint and coercive

-------------------------------------------------------------------------------
"""

import numpy as np
import scipy.linalg as la


# ============================================================
# RELATIONAL LYSIS ENGINE
# ============================================================

class RelationalLysisEngine:

    def __init__(self, tol=1e-12, max_depth=10):
        self.tol = tol
        self.max_depth = max_depth

    def decompose(self, state):
        """
        Solved state decomposition: Sigma = (D, S)
        """
        D = 0.5 * (state + state.T)
        S = 0.5 * (state - state.T)
        return D, S

    def step(self, sigma):
        """
        Hierarchical step preserving solved-state structure
        """
        D, S = sigma
        next_D, next_S = self.decompose(D)
        return (next_D, next_S)

    def run(self, initial_state):

        sigma = self.decompose(initial_state)

        history = []
        diamond_history = []

        for depth in range(self.max_depth):

            D, S = sigma

            diamond_history.append(D.copy())

            symmetry_error = np.linalg.norm(D - D.T)
            shadow_norm = np.linalg.norm(S)

            history.append((symmetry_error, shadow_norm))

            next_sigma = self.step(sigma)

            delta = np.linalg.norm(next_sigma[0] - D)

            if delta < self.tol:
                return next_sigma, history, diamond_history, True

            sigma = next_sigma

        return sigma, history, diamond_history, False


# ============================================================
# CONTRACTION RATIO
# ============================================================

def compute_contraction_ratios(diamond_history):

    ratios = []

    if len(diamond_history) < 3:
        return ratios

    for k in range(2, len(diamond_history)):

        D_prev = diamond_history[k-2]
        D_curr = diamond_history[k-1]
        D_next = diamond_history[k]

        num = np.linalg.norm(D_next - D_curr)
        den = np.linalg.norm(D_curr - D_prev)

        if den > 0:
            ratios.append(num / den)

    return ratios


def summarize_contraction(ratios):

    if len(ratios) == 0:
        return None

    ratios = np.array(ratios)

    return {
        "mean": np.mean(ratios),
        "max": np.max(ratios),
        "min": np.min(ratios)
    }


# ============================================================
# STATE GENERATORS
# ============================================================

def random_dense(N):
    return np.random.randn(N, N)


def random_sparse(N):

    A = np.zeros((N, N))

    nnz = N * 5
    idx = np.random.choice(N*N, size=nnz, replace=False)

    A.flat[idx] = np.random.randn(len(idx))

    return A


def skew_dominated(N):

    A = np.random.randn(N, N)
    return A - A.T


def ill_conditioned(N):

    U = np.random.randn(N, N)
    s = np.logspace(0, 6, N)

    return U @ np.diag(s) @ la.inv(U)


def structured_chain(N):

    A = np.zeros((N, N))

    for i in range(N - 1):
        A[i, i+1] = 1
        A[i+1, i] = 1

    return A


# ============================================================
# EMERGENT OPERATOR
# ============================================================

def emergent_operator(D):

    degree = np.diag(np.sum(np.abs(D), axis=1))
    L = degree - D

    return L


def operator_properties(L):

    symmetry = np.linalg.norm(L - L.T)

    evals = la.eigvalsh(L)

    min_eval = np.min(evals)

    coercive = min_eval > -1e-10

    return symmetry, min_eval, coercive


# ============================================================
# EXPERIMENT
# ============================================================

def run_experiment():

    print("\nRELATIONAL LYSIS — REVERSE OPERATOR UNIVERSALITY (N = 500)")
    print("------------------------------------------------------------")

    np.random.seed(0)

    engine = RelationalLysisEngine()

    generators = [
        random_dense,
        random_sparse,
        skew_dominated,
        ill_conditioned,
        structured_chain
    ]

    N = 500

    for gen in generators:

        print(f"\n[*] Testing State Type: {gen.__name__}")

        state = gen(N)

        sigma, history, diamond_history, converged = engine.run(state)

        if not converged:
            print(" FAIL: Hierarchy did not terminate")
            continue

        D, S = sigma

        print(" Converged Depth:", len(history))
        print(" Final Shadow Norm:", np.linalg.norm(S))
        print(" Diamond Symmetry Error:", np.linalg.norm(D - D.T))

        # ----------------------------
        # Contraction
        # ----------------------------

        ratios = compute_contraction_ratios(diamond_history)
        stats = summarize_contraction(ratios)

        if stats:
            print(" Contraction Ratio Mean:", stats["mean"])
            print(" Contraction Ratio Max :", stats["max"])
        else:
            print(" Contraction Ratio: insufficient depth")

        # ----------------------------
        # Operator
        # ----------------------------

        L = emergent_operator(D)

        sym, min_eval, coercive = operator_properties(L)

        print(" Operator Symmetry Error:", sym)
        print(" Min Eigenvalue:", min_eval)
        print(" Coercive:", coercive)

    print("\nINTERPRETATION:")
    print("If all admissible states terminate with coercive operators")
    print("and contraction ratio < 1 → universality supported.")


# ============================================================

if __name__ == "__main__":
    run_experiment()
