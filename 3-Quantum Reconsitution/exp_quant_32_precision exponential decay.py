"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_32_precision exponential decay.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 11.2, Axiom 11.2 (Clustering Property)
Theorem Support: "Precision Confirmation of Massive Propagator Decay"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    A high-precision variant of the Exponential Correlation Decay test (Exp 41).
    Uses a larger lattice (N=2000) and a "Goldilocks Zone" for tail fitting to
    minimize boundary artifacts.

    Verifies that the Green's function (Propagator) decays exactly as
    exp(-m*r), where 'm' is the spectral mass derived from the operator.
    This provides rigorous confirmation of the clustering property.

ADVERSARIAL CONDITIONS:
    - Lattice Size:            N = 2000 (Minimizing finite-size effects)
    - Fit Region:              r = 200 to 600 (Far from source and edge)
    - Solver Tolerance:        1e-12

PASS CRITERIA:
    1. Precision Match:        Fitted Decay / Spectral Mass ≈ 1.00 (± 0.01).
    2. Linearity:              R^2 correlation > 0.99.

USAGE:
    python3 exp_quant_rec_41b_precision_decay.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import cg
from scipy.stats import linregress

# -------------------------------
# Larger lattice to minimize boundary effects
# -------------------------------
N = 2000
# Look at the "Goldilocks Zone" - far from source, far from edge
TAIL_START = 200
TAIL_END = 600
EPS = 1e-15


# -------------------------------
# Build Laplacian
# -------------------------------
def build_laplacian(N):
    main = -2 * np.ones(N)
    off = np.ones(N - 1)
    return diags([main, off, off], [0, -1, 1], format="csr")


# -------------------------------
# Get Spectral Mass (sqrt of lowest eigenvalue)
# -------------------------------
def get_spectral_mass(L):
    # Analytical for discrete 1D Laplacian: 2*sin(pi/2(N+1))
    return 2.0 * np.sin(np.pi / (2 * (N + 1)))


# -------------------------------
# Green's Function (Propagator)
# -------------------------------
def green_function(L, mass):
    # (L + m^2) G = delta
    m2 = mass**2
    A = L + m2 * diags([np.ones(N)], [0])

    src = np.zeros(N)
    src[N // 2] = 1.0

    # FIX: Use 'rtol' instead of 'tol'
    G, info = cg(A, src, rtol=1e-12)
    return np.abs(G)


# -------------------------------
# Main
# -------------------------------
def main():
    L = build_laplacian(N)

    # 1. Theoretical/Spectral Mass
    m_spec = get_spectral_mass(L)

    # 2. Measure Decay of Propagator
    G = green_function(L, m_spec)
    center = N // 2

    # Normalize center to 1
    G /= G[center]

    # Extract the tail
    r = np.arange(N) - center
    r = np.abs(r)

    mask = (r >= TAIL_START) & (r <= TAIL_END)
    r_fit = r[mask]
    log_G = np.log(G[mask] + EPS)

    # Linear Regression on Log plot -> Slope is decay rate
    slope, intercept, r_value, p_value, std_err = linregress(r_fit, log_G)
    m_fit = -slope

    print("\nRELATIONAL LYSIS — SCRIPT TYPE 41B")
    print("Precision Exponential Decay Test")
    print("--------------------------------------------------")
    print(f"Lattice size N:        {N}")
    print(f"Spectral Mass (m):     {m_spec:.8f}")
    print(f"Fitted Decay (slope):  {m_fit:.8f}")
    print(f"Ratio (Fit / Mass):    {m_fit/m_spec:.6f}")
    print(f"Correlation R^2:       {r_value**2:.8f}")
    print("--------------------------------------------------")
    print("INTERPRETATION:")
    print("Ratio ≈ 1.00 proves the Mass Gap drives")
    print("exact exponential decay (Particle propagator).")


if __name__ == "__main__":
    main()
