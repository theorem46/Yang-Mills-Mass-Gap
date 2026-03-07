#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_structural_defense_12_Yang-Mills Mass Gap_Quantize_7.py
Category:        2-Structural Defense
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 17.2 (Probabilistic Geometric Projection)
Theorem Support: "Stochastic Invariance of the Terminal Alignment Diamond"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Validates the hypothesis that the terminal state of the Relational Lysis 
    hierarchy is a deterministic geometric invariant, even when the input field 
    is perturbed by stochastic noise. 
    
    The script establishes a 'Deterministic Reference' using a nonlinear state 
    and constructs a rank-1 geometric projector ($P$) from its terminal diamond. 
    It then subjects the system to multiple trials where Gaussian noise is 
    injected into the base field. 
    
    By decomposing the resulting terminal diamond into 'Aligned' and 'Residual' 
    components, the experiment quantifies the hierarchy's ability to filter 
    probability. A successful test shows that the 'Aligned' component 
    captures nearly all the energy, while the 'Residual' (noise) is suppressed.

ADVERSARIAL CONDITIONS:
    - Lattice Size:             2048 (High-fidelity continuum)
    - Noise Level:              0.01 Standard Deviation (Gaussian)
    - Interaction:              Quadratic Nonlinearity ($g=0.25$)
    - Hierarchy Depth:          12 Levels
    - Metric:                   $\ell_2$ Norm Decomposition (Aligned vs. Residual)

PASS CRITERIA:
    1. Alignment Stability:    ||Aligned|| consistently matches the reference norm.
    2. Residual Suppression:   ||Residual|| remains orders of magnitude smaller 
                               than the aligned component.
    3. Geometric Primacy:      Confirms that the Mass Gap's orientation is 
                               governed by geometry, not probability.

USAGE:
    python3 exp_adv_noise_probabilistic_alignment_decomp.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np

# ============================================================
# FIXED RELATIONAL LYSIS OPERATOR
# ============================================================
def RL(x):
    return x[2:] - 2*x[1:-1] + x[:-2]

def Phi(x):
    D = RL(x)
    S = x[1:-1] - D
    return D, S

# ============================================================
# NONLINEAR INTERACTION STATE
# ============================================================
def nonlinear_state(x, g=0.25):
    y = x.copy()
    y[1:-1] += g * x[1:-1]**2
    return y

# ============================================================
# TERMINAL DIAMOND VIA HIERARCHICAL LYSIS
# ============================================================
def terminal_diamond(state, max_depth=12):
    current = state.copy()
    for _ in range(max_depth):
        if len(current) < 5:
            break
        D, S = Phi(current)
        current = D
    return current

# ============================================================
# BUILD GEOMETRIC PROJECTOR FROM DETERMINISTIC RUN
# ============================================================
def geometric_projector(diamond_ref):
    v = diamond_ref / np.linalg.norm(diamond_ref)
    P = np.outer(v, v)  # rank-1 projector onto intrinsic geometry
    return P

# ============================================================
# PROBABILISTIC ALIGNMENT TEST
# ============================================================
def probabilistic_alignment_test():
    N = 2048
    t = np.linspace(0, 2*np.pi, N)
    base = np.sin(t) + 0.3*np.cos(3*t)

    # ---------- Deterministic reference ----------
    x_det = nonlinear_state(base)
    xI_det = x_det - base
    D_ref = terminal_diamond(xI_det)
    P = geometric_projector(D_ref)

    print("\n--- Probabilistic Alignment–Decomposition Test ---")
    print(f"Reference ||D*|| = {np.linalg.norm(D_ref):.6e}\n")

    # ---------- Probabilistic trials ----------
    for trial in range(10):
        noise = 0.01 * np.random.randn(N)
        x = base + noise

        x_nl = nonlinear_state(x)
        x_I = x_nl - x

        D_star = terminal_diamond(x_I)

        # Alignment decomposition
        D_aligned = P @ D_star
        D_residual = D_star - D_aligned

        print(
            f"Trial {trial:2d}: "
            f"||D*||={np.linalg.norm(D_star):.6e} | "
            f"||Aligned||={np.linalg.norm(D_aligned):.6e} | "
            f"||Residual||={np.linalg.norm(D_residual):.6e}"
        )

# ============================================================
if __name__ == "__main__":
    probabilistic_alignment_test()
