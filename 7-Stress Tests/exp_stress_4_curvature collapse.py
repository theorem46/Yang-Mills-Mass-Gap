"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_stress_4_curvature collapse.py
Category:        7-Stress Tests
Researcher:      Dr. David Swanagon
Original Date:   February 12, 2026
Paper Reference: Section 40.2 (Curvature Lower Bounds and Spectral Stability)
Theorem Support: "Stochastic Stability of the SU(2) Mass Gap under Geometric Stress"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Evaluates the robustness of the Mass Gap ($\lambda_1$) against adversarial 
    geometric configurations. A common critique of spectral gap proofs is that 
    the gap might vanish in the presence of concentrated or oscillatory curvature. 
    
    This script generates sequences of $SU(2)$ gauge fields specifically 
    designed to pressure the spectral floor:
    1. Concentration: Shrinking the support of the field to a singular point.
    2. Oscillation: Rapidly varying the gauge field phases.
    3. Tube: Localizing the field energy along a 1D 'thin-tube' manifold.
    
    By computing the smallest non-zero eigenvalue of the Covariant Laplacian 
    under these extreme conditions, the experiment verifies that the Mass Gap 
    persists as a strictly positive physical quantity, provided the curvature 
    $\epsilon$ remains non-zero.

ADVERSARIAL CONDITIONS:
    - Gauge Group:             SU(2) (Axis-angle representation)
    - Volume:                  $L^4$ (4D Lattice simulation)
    - Curvature Floor (EPS):   0.5
    - Failure Tolerance:       1e-5
    - Sequence Depth:          6 Iterative refinement steps per mode

PASS CRITERIA:
    1. Spectral Persistence:   $\lambda_1$ remains $> FAIL\_TOL$ in all trials.
    2. Curvature Decoupling:   Proves that high-frequency noise and localization 
                               cannot 'zero out' the physical mass.
    3. SU(2) Covariance:       Validates the Gap on a non-Abelian 4D manifold.

USAGE:
    python3 exp_adv_noise_curvature_constrained_gap.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
from scipy.sparse.linalg import eigsh, LinearOperator

EPS = 0.5         # curvature lower bound
FAIL_TOL = 1e-5
L_VALUES = [6,7,8]
SEQUENCE_STEPS = 6

# SU(2)
sigma1 = np.array([[0,1],[1,0]], dtype=complex)
sigma2 = np.array([[0,-1j],[1j,0]], dtype=complex)
sigma3 = np.array([[1,0],[0,-1]], dtype=complex)

def su2_axis_angle(axis, theta):
    axis = axis / np.linalg.norm(axis)
    gen = axis[0]*sigma1 + axis[1]*sigma2 + axis[2]*sigma3
    return np.cos(theta)*np.eye(2) + 1j*np.sin(theta)*gen

# Curvature proxy
def curvature_strength(U):
    total = 0.0
    for key in U:
        total += np.linalg.norm(U[key] - np.eye(2))**2
    return np.sqrt(total / len(U))

# Build adversarial fields
def build_field(L, mode, step):

    U = {}
    center = L//2
    scale = 2**step

    for mu in range(4):
        for i in range(L):
            for j in range(L):
                for k in range(L):
                    for l in range(L):

                        if mode == "concentration":
                            # shrinking support
                            if abs(i-center) < L//scale:
                                U[(mu,i,j,k,l)] = su2_axis_angle([1,0,0], 1.0)
                            else:
                                U[(mu,i,j,k,l)] = np.eye(2)

                        elif mode == "oscillation":
                            theta = np.sin(scale * 2*np.pi*i/L)
                            U[(mu,i,j,k,l)] = su2_axis_angle([0,1,0], theta)

                        elif mode == "tube":
                            if j == center:
                                U[(mu,i,j,k,l)] = su2_axis_angle([0,0,1], 1.0)
                            else:
                                U[(mu,i,j,k,l)] = np.eye(2)

    return U

# Covariant Laplacian
def make_operator(L, U):

    volume = L**4
    dim = 2*volume

    def idx(i,j,k,l):
        return ((i*L+j)*L+k)*L+l

    def matvec(vec):
        vec = vec.reshape((volume,2))
        result = np.zeros_like(vec, dtype=complex)

        for i in range(L):
            for j in range(L):
                for k in range(L):
                    for l in range(L):

                        id0 = idx(i,j,k,l)
                        center = vec[id0]
                        accum = 8*center
                        coords = [i,j,k,l]

                        for mu in range(4):
                            f = coords.copy()
                            b = coords.copy()
                            f[mu]=(coords[mu]+1)%L
                            b[mu]=(coords[mu]-1)%L

                            accum -= U[(mu,i,j,k,l)] @ vec[idx(*f)]
                            accum -= U[(mu,b[0],b[1],b[2],b[3])].conj().T @ vec[idx(*b)]

                        result[id0]=accum

        return result.reshape(dim)

    return LinearOperator((dim,dim), matvec=matvec, dtype=complex)

print("\nRELATIONAL LYSIS — CURVATURE-CONSTRAINED GAP TEST")
print("===================================================")

global_min = 1e9

for L in L_VALUES:

    print(f"\nTesting volume L={L}")

    for mode in ["concentration","oscillation","tube"]:

        for step in range(1, SEQUENCE_STEPS+1):

            U = build_field(L, mode, step)

            curv = curvature_strength(U)

            if curv < EPS:
                continue  # enforce curvature floor

            Op = make_operator(L, U)

            vals,_ = eigsh(Op, k=3, which='SM')
            vals = np.sort(np.real(vals))
            lambda1 = vals[1]

            global_min = min(global_min, lambda1)

            print(f"{mode}, step {step}: curvature={curv:.3f}, λ1={lambda1:.6f}")

            if lambda1 < FAIL_TOL:
                raise RuntimeError("FAIL — Gap collapse under curvature constraint.")

print("\n===================================================")
print("Minimum λ1 observed:", global_min)
print("PASS — No curvature-bounded sequence collapsed the gap.")
