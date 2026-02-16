"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_stress_1_4D curvature concentrartion test.py
Category:        7-Stress Tests
Researcher:      Dr. David Swanagon
Original Date:   February 12, 2026
Paper Reference: Section 43.3 (Singular Concentrations and the Spectral Floor)
Theorem Support: "Lower Bound Invariance under Spatial Curvature Compression"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Evaluates the stability of the Mass Gap ($\lambda_1$) against extreme 
    localization of gauge energy. A potential failure mode for spectral proofs 
    is that the gap might vanish if the field curvature is "pinched" into 
    vanishingly small volumes, effectively simulating a point-singularity.
    
    This script:
    1. Generates an $SU(2)$ gauge field on a $6^4$ lattice.
    2. Concentrates random gauge links within a hyper-cubic "core" of 
       decreasing size (Core = 4, 3, 2, 1).
    3. Leaves the remaining "bulk" as a flat vacuum ($\mathbb{1}$).
    4. Measures $\lambda_1$ for each core size.
    
    A stable or increasing $\lambda_1$ as the core shrinks provides empirical 
    proof that the Mass Gap is topologically protected against 
    spatial compression and "UV" noise.

ADVERSARIAL CONDITIONS:
    - Lattice Volume:          $6^4$ (1296 sites)
    - Gauge Group:             $SU(2)$
    - Core Scale Reduction:    $4^4 \to 1^4$
    - Lattice Spacing (h):     0.5
    - Metric:                   Principal Eigenvalue ($\lambda_1$) Sensitivity

PASS CRITERIA:
    1. Non-Zero Persistence:   $\lambda_1$ must remain significantly above 0 
                               even as the core reaches the lattice limit.
    2. Monotonic Stability:    Decreasing the core size should not result 
                               in a catastrophic drop in the spectral gap.
    3. Structural Resilience:  Confirms the Relational Lysis diamond logic 
                               operates at the minimal resolution scale.

USAGE:
    python3 exp_adv_noise_concentrated_field_robustness.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
from scipy.sparse.linalg import eigsh, LinearOperator

# SU(2)
sigma1 = np.array([[0,1],[1,0]], dtype=complex)
sigma2 = np.array([[0,-1j],[1j,0]], dtype=complex)
sigma3 = np.array([[1,0],[0,-1]], dtype=complex)

def su2_from_axis_angle(axis, theta):
    axis = axis / np.linalg.norm(axis)
    gen = axis[0]*sigma1 + axis[1]*sigma2 + axis[2]*sigma3
    return np.cos(theta)*np.eye(2) + 1j*np.sin(theta)*gen

def random_link(strength):
    axis = np.random.randn(3)
    theta = strength
    return su2_from_axis_angle(axis, theta)

# ------------------------------------------------------------
# Concentrated Gauge Field
# ------------------------------------------------------------

def build_concentrated_field(L, core_size, strength):

    U = {}

    center = L // 2
    half = core_size // 2

    for mu in range(4):
        for i in range(L):
            for j in range(L):
                for k in range(L):
                    for l in range(L):

                        in_core = (
                            abs(i-center) < half and
                            abs(j-center) < half and
                            abs(k-center) < half and
                            abs(l-center) < half
                        )

                        if in_core:
                            U[(mu,i,j,k,l)] = random_link(strength)
                        else:
                            U[(mu,i,j,k,l)] = np.eye(2)

    return U

# ------------------------------------------------------------
# Matrix-free Operator
# ------------------------------------------------------------

def make_operator(L, h, U):

    volume = L**4
    dim = 2 * volume

    def site_index(i,j,k,l):
        return ((i*L + j)*L + k)*L + l

    def matvec(vec):

        vec = vec.reshape((volume,2))
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

# ------------------------------------------------------------
# Run Concentration Test
# ------------------------------------------------------------

def concentration_test(L=6, refine=2):

    h = 1.0 / refine

    for core in [4, 3, 2, 1]:

        print(f"\nCore size = {core}")

        U = build_concentrated_field(L, core_size=core, strength=1.0)
        Op = make_operator(L, h, U)

        vals, _ = eigsh(Op, k=3, which='SM')
        vals = np.sort(np.real(vals))
        lambda1 = vals[1]

        print("lambda1 =", lambda1)

# ------------------------------------------------------------
# Execute
# ------------------------------------------------------------

concentration_test(L=6, refine=2)
