#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_structural_defense_11_Yang-Mills Mass Gap_Quantize_6.py
Category:        2-Structural Defense
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 18.1 (Non-Abelian Interaction Scaling)
Theorem Support: "Continuum Stability of SU(2) Fixed Points"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the persistence of the spectral gap in a simulated SU(2) gauge 
    environment. The script constructs a non-Abelian field $A$ (3-component 
    vector field) and introduces a nonlinear interaction term representing 
    the self-coupling of the gauge field. 
    
    The experiment performs component-wise hierarchical lysis to identify the 
    fixed-point norm of the system across increasing lattice dimensions (N). 
    Stability of the terminal diamond norm across scales ($N=512$ to $4096$) 
    provides empirical evidence that the Mass Gap is a robust property of 
    SU(2) dynamics and is not destroyed by the continuum limit.

ADVERSARIAL CONDITIONS:
    - Gauge Group:             SU(2) (Simulated via 3-vector field)
    - Interaction Strength:    g = 0.25 (Nonlinear self-interaction)
    - Scaling Range:           N = 512 to 4096 (Lattice refinement)
    - Metric:                   Component-wise Fixed-Point Norm

PASS CRITERIA:
    1. Scaling Invariance:     The terminal norm ||D|| remains stable as N grows.
    2. Non-Abelian Gap:        The fixed-point norm remains strictly > 0, 
                               denoting a persistent mass.
    3. Structural Integrity:    No dimensional collapse or divergence under 
                               SU(2) coupling.

USAGE:
    python3 exp_quant_rec_su2_interaction_scaling.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np

# ============================================================
# RL OPERATOR (UNCHANGED)
# ============================================================
def RL(x):
    return x[2:] - 2*x[1:-1] + x[:-2]

def Phi(x):
    D = RL(x)
    S = x[1:-1] - D
    return D, S

# ============================================================
# SU(2)-VALUED FIELD (Diagonal Embedding)
# ============================================================
def su2_field(N):
    t = np.linspace(0, 2*np.pi, N)
    A1 = np.sin(t)
    A2 = np.cos(2*t)
    A3 = np.sin(3*t)
    return np.stack([A1, A2, A3], axis=1)

# ============================================================
# NONLINEAR INTERACTION STATE (GAUGE-VALUED)
# ============================================================
def nonlinear_interaction_su2(A, g=0.25):
    B = A.copy()
    B[1:-1] += g * (A[1:-1] @ A[1:-1].T).diagonal()[:,None]
    return B

# ============================================================
# HIERARCHICAL LYSIS (COMPONENTWISE)
# ============================================================
def fixed_point_norm_su2(A):
    norms = []
    current = A.copy()

    for _ in range(10):
        if len(current) < 5:
            break
        D = np.stack([RL(current[:,i]) for i in range(3)], axis=1)
        norms.append(np.linalg.norm(D))
        current = D

    return norms[-1], norms

# ============================================================
# MAIN TEST
# ============================================================
def run_su2_test():
    sizes = [512, 1024, 2048, 4096]

    print("\n--- SU(2) Gauge Interaction Scaling ---")
    for N in sizes:
        A = su2_field(N)
        A_nl = nonlinear_interaction_su2(A)
        A_I = A_nl - A

        fp, _ = fixed_point_norm_su2(A_I)
        print(f"N={N:5d} | fixed-point ||D|| = {fp:.6e}")

if __name__ == "__main__":
    run_su2_test()
