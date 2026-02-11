"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_31_exponential correlation decay.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 11.2, Axiom 11.2 (Clustering Property)
Theorem Support: "Exponential Clustering (Massive Propagator)"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests for the "Clustering Property" (Wightman Axiom) by measuring the
    Green's function (Propagator) of the Relational Lysis operator.

    A massive theory must exhibit exponential decay G(r) ~ exp(-m*r).
    This script fits the decay rate and compares it to the input spectral mass.
    A match confirms the theory describes massive particles, not long-range forces.

ADVERSARIAL CONDITIONS:
    - Lattice Size:            N = 800
    - Tail Fit Region:         r = 120 to 350
    - Precision:               1e-12

PASS CRITERIA:
    1. Linearity:              Log(G(r)) is linear (R^2 > 0.99).
    2. Mass Match:             Fitted_Mass / Lattice_Mass ≈ 1.0.

USAGE:
    python3 exp_quant_rec_41_exponential_decay.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh, cg
from scipy.stats import linregress

# -------------------------------
N = 800
TAIL_START = 120
TAIL_END = 350
EPS = 1e-12


# -------------------------------
def build_laplacian(N):
    main = -2 * np.ones(N)
    off = np.ones(N - 1)
    return diags([main, off, off], [0, -1, 1], format="csr")


# -------------------------------
def spectral_gap(L):
    vals = eigsh(L, k=2, which="SM", return_eigenvectors=False)
    return abs(vals[1])


# -------------------------------
def lattice_mass(N):
    return 2 * np.sin(np.pi / (2 * N))


# -------------------------------
def green_column(L, m2):
    A = L + m2 * diags([np.ones(N)], [0])
    src = np.zeros(N)
    src[N // 2] = 1.0
    G,_ = cg(A, src, atol=1e-10)
    return G


# -------------------------------
def main():

    L = build_laplacian(N)

    lam1 = spectral_gap(L)
    m_spec = np.sqrt(lam1)
    m_lat = lattice_mass(N)

    G = np.abs(green_column(L, lam1))
    center = N // 2
    G /= G[center]

    r = np.abs(np.arange(N) - center)

    mask = (r >= TAIL_START) & (r <= TAIL_END)
    slope, _, rval, _, _ = linregress(r[mask], np.log(G[mask] + EPS))
    m_fit = -slope

    print("\nRELATIONAL LYSIS — SCRIPT TYPE 41 (ULTRA TIGHT)")
    print("Exponential Correlation Decay Test")
    print("--------------------------------------------------")
    print(f"Lattice size N:                {N}")
    print(f"sqrt(lambda1):                 {m_spec:.10f}")
    print(f"Lattice-theory mass:           {m_lat:.10f}")
    print(f"Fitted decay constant:         {m_fit:.10f}")
    print(f"Fit / sqrt(lambda1):           {m_fit/m_spec:.6f}")
    print(f"Fit / lattice-mass:            {m_fit/m_lat:.6f}")
    print(f"Correlation R^2:               {rval**2:.10f}")
    print("")

    print("Sample tail:")
    for i in [TAIL_START, 200, 300]:
        idx = center + i
        print(f"r={i:<4d}  G(r)={G[idx]:.6e}")

    print("--------------------------------------------------")
    print("INTERPRETATION:")
    print("If Fit / lattice-mass ≈ 1 and R^2 ≈ 1:")
    print("Relational Lysis produces exponential clustering.")
    print("Mass gap is physical.")


# -------------------------------
if __name__ == "__main__":
    main()
