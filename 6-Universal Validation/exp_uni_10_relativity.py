#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

import numpy as np

np.set_printoptions(precision=6, suppress=True)

# ============================================================
# RL SOLVED STATE
# ============================================================

def sym(M):
    M = (M + M.T) / 2.0
    np.fill_diagonal(M, 0.0)
    return M

class SolvedState:
    def __init__(self, D, S):
        self.D = sym(D)
        self.S = sym(S)

# ============================================================
# RL-LEGAL LYSIS (NO CHEATING)
# ============================================================
# Rules enforced:
# 1. Lysis acts on (D + S), not D alone
# 2. Shadow is transported, not recomputed
# 3. Shadow never generates alignment
# 4. No normalization or metric fixing

def lysis_A(X):
    D, S = X.D, X.S
    J = D + S

    # alignment extraction constrained to prior diamond support
    Dn = sym(D @ J)

    # shadow trace accumulates only what fails alignment
    Sn = sym(S + (J - Dn))

    return SolvedState(Dn, Sn)

def lysis_B(X):
    D, S = X.D, X.S
    J = D + S

    # different admissible contraction, still diamond-constrained
    Dn = sym(J @ D)

    Sn = sym(S + (J - Dn))

    return SolvedState(Dn, Sn)

def run_lysis(X, op, depth=50):
    Y = X
    for _ in range(depth):
        Y = op(Y)
    return Y

# ============================================================
# RL-INTERNAL SIGNATURE (NO REPRESENTATION BIAS)
# ============================================================

def stable_rank(M, eps=1e-12):
    s = np.linalg.svd(M, compute_uv=False)
    return (np.sum(s)**2) / (np.sum(s*s) + eps)

def rl_signature(X):
    eig = np.linalg.eigvalsh(X.D)
    return {
        "D_norm": np.sqrt(np.sum(X.D * X.D)),
        "S_norm": np.sqrt(np.sum(X.S * X.S)),
        "stable_rank": stable_rank(X.D),
        "eig_min": eig.min(),
        "eig_max": eig.max()
    }

def equivalent(sig1, sig2, tol=1e-6):
    for k in sig1:
        if abs(sig1[k] - sig2[k]) > tol:
            return False
    return True

# ============================================================
# INITIAL SOLVED STATE (SINGLE SOURCE)
# ============================================================

np.random.seed(11)
N = 20

D0 = sym(np.random.randn(N, N))
S0 = sym(np.random.randn(N, N))

X0 = SolvedState(D0, S0)

# ============================================================
# HARMONIC NON-UNIQUENESS KILL TEST
# ============================================================

XA = run_lysis(X0, lysis_A)
XB = run_lysis(X0, lysis_B)

sigA = rl_signature(XA)
sigB = rl_signature(XB)

print("\n--- Harmonic Endpoint A ---")
for k in sigA:
    print(f"{k:12s} : {sigA[k]: .6f}")

print("\n--- Harmonic Endpoint B ---")
for k in sigB:
    print(f"{k:12s} : {sigB[k]: .6f}")

print("\n--- RL KILL TEST RESULT ---")
print("Equivalent endpoints:", equivalent(sigA, sigB))
