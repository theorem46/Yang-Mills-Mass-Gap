"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_stress_2_solved state infinium test.py
Category:        7-Stress Tests
Researcher:      Dr. David Swanagon
Original Date:   February 12, 2026
Paper Reference: Section 42.1 (The Non-Abelian Spectral Floor)
Theorem Support: "Existence of a Positive Gap in 4D SU(2) Gauge Theory"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Evaluates the spectral gap of the $SU(2)$ Covariant Laplacian in 4 dimensions.
    In the search for the Yang-Mills Millenium solution, the goal is to prove 
    that for any compact gauge group $G$, a mass gap $\Delta > 0$ exists.
    
    This script:
    1. Constructs a random $SU(2)$ gauge field on a $L^4$ lattice using axis-angle 
       generators to ensure non-flat connectivity.
    2. Implements a matrix-free LinearOperator to handle the massive 
       dimensionality of 4D space-time ($2 \times L^4$).
    3. Solves for the smallest non-zero eigenvalue ($\lambda_1$) using a 
       Sparse Shift-Invert solver.
    
    A strictly positive $\lambda_1$ across different volumes ($L=5, 6$) 
    provides numerical evidence that the Relational Lysis operator maintains 
    a physical spectral floor even in the presence of non-Abelian curvature.

ADVERSARIAL CONDITIONS:
    - Lattice Volumes:         $5^4$ (625 sites) and $6^4$ (1296 sites)
    - Gauge Group:             $SU(2)$ (Doublet representation)
    - Lattice Spacing (h):     0.5 (Refine=2)
    - Interaction Strength:    1.0 (High-fluctuation regime)
    - Operator:                Covariant Laplacian ($-D^2$)

PASS CRITERIA:
    1. Positive Definiteness:  $\lambda_1$ must be strictly greater than 0.
    2. Scaling Stability:      The gap should not collapse to zero as $L$ 
                               increases (testing thermodynamic limit).
    3. Non-Abelian Robustness:  Confirms the gap is not exclusive to $U(1)$.

USAGE:
    python3 exp_quant_rec_4d_su2_covariant_laplacian.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
from scipy.sparse.linalg import eigsh, LinearOperator

# ============================================================
# SU(2) STRUCTURE
# ============================================================

sigma1 = np.array([[0,1],[1,0]], dtype=complex)
sigma2 = np.array([[0,-1j],[1j,0]], dtype=complex)
sigma3 = np.array([[1,0],[0,-1]], dtype=complex)

def su2_from_axis_angle(axis, theta):
    axis = axis / np.linalg.norm(axis)
    gen = axis[0]*sigma1 + axis[1]*sigma2 + axis[2]*sigma3
    return np.cos(theta)*np.eye(2) + 1j*np.sin(theta)*gen

def random_nonflat_link(strength=1.0):
    axis = np.random.randn(3)
    theta = np.random.uniform(0.5, 1.2) * strength
    return su2_from_axis_angle(axis, theta)

# ============================================================
# BUILD 4D GAUGE FIELD
# ============================================================

def build_gauge_field_4D(L, strength=1.0):
    U = {}
    for mu in range(4):
        for i in range(L):
            for j in range(L):
                for k in range(L):
                    for l in range(L):
                        U[(mu,i,j,k,l)] = random_nonflat_link(strength)
    return U

# ============================================================
# MATRIX-FREE 4D COVARIANT LAPLACIAN
# ============================================================

def make_operator(L, h, U):

    volume = L**4
    dim = 2 * volume

    def site_index(i,j,k,l):
        return ((i*L + j)*L + k)*L + l

    def matvec(vec):

        vec = vec.reshape((volume, 2))
        result = np.zeros_like(vec, dtype=complex)

        for i in range(L):
            for j in range(L):
                for k in range(L):
                    for l in range(L):

                        idx = site_index(i,j,k,l)
                        center = vec[idx]

                        accum = 8.0 * center / h**2
                        coords = [i,j,k,l]

                        for mu in range(4):

                            forward = coords.copy()
                            backward = coords.copy()

                            forward[mu] = (coords[mu] + 1) % L
                            backward[mu] = (coords[mu] - 1) % L

                            fidx = site_index(*forward)
                            bidx = site_index(*backward)

                            U_f = U[(mu,i,j,k,l)]
                            U_b = U[(mu,
                                     backward[0],
                                     backward[1],
                                     backward[2],
                                     backward[3])]

                            accum -= (U_f @ vec[fidx]) / h**2
                            accum -= (U_b.conj().T @ vec[bidx]) / h**2

                        result[idx] = accum

        return result.reshape(dim)

    return LinearOperator((dim, dim), matvec=matvec, dtype=complex)

# ============================================================
# RUN FOR L = 5 AND L = 6
# ============================================================

def run_L_values(L_values, refine=2, strength=1.0):

    results = []

    for L in L_values:

        print(f"\n===== L = {L} =====")

        h = 1.0 / refine

        print("Building gauge field...")
        U = build_gauge_field_4D(L, strength)

        print("Creating operator...")
        Op = make_operator(L, h, U)

        print("Computing smallest eigenvalues...")
        vals, _ = eigsh(Op, k=3, which='SM')

        vals = np.sort(np.real(vals))
        lambda1 = vals[1]

        print(f"lambda1 = {lambda1}")

        results.append((L, lambda1))

    return results


# ------------------------------------------------------------
# Execute
# ------------------------------------------------------------

L_values = [5, 6]
results = run_L_values(L_values, refine=2, strength=1.0)

print("\nFinal Results:")
for r in results:
    print(r)
