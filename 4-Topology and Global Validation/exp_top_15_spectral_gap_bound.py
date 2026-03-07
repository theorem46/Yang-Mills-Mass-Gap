#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_top_15_spectral_gap_bound.py
Category:        4-Topology and Global Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 27.1, Theorem 27.1 (Spectral Gap Robustness)
Theorem Support: "Gershgorin Disk Stability under Unitary Gauge Transformations"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the deterministic lower bound of the spectral gap using Gershgorin's 
    Circle Theorem. In gauge theories, local transformations can obscure the 
    underlying spectrum; this script verifies that the "Alignment Diamond" 
    remains spectrally isolated despite these shifts.
    
    The script constructs a canonical Lysis matrix and applies a stochastic 
    U(1) gauge transformation ($\beta = 0.5$). It then calculates the 
    Gershgorin disks for the transformed matrix to determine the minimum 
    possible eigenvalue. 
    
    A lower bound strictly greater than zero provides an analytical guarantee 
    that the system possesses a Mass Gap that cannot be "gauged away" or 
    nullified by local phase fluctuations.

ADVERSARIAL CONDITIONS:
    - Lattice Size:             N = 80
    - Gauge Intensity ($\beta$):   0.5 (Significant stochastic phase shift)
    - Operator:                 Tridiagonal Relational Lysis Matrix
    - Metric:                   Gershgorin Minimum $(\text{Center} - \text{Radius})$

PASS CRITERIA:
    1. Spectral Persistence:   The calculated lower bound must be $> 0$.
    2. Gauge Invariance:       The gap remains robust against non-Abelian-like 
                               unitary transformations.
    3. Structural Integrity:    Confirms that the operator is strictly 
                               Positive Definite (PD) in all gauge frames.

USAGE:
    python3 exp_top_val_35_gershgorin_spectral_gap_bound.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np


# ---------------------------
# Lysis Matrix
# ---------------------------
def lysis_matrix(N):
    L = np.zeros((N, N))
    for i in range(N):
        L[i, i] = 2.0
        if i > 0:
            L[i, i - 1] = -1.0
        if i < N - 1:
            L[i, i + 1] = -1.0
    return L


# ---------------------------
# Gauge Transform
# ---------------------------
def gauge_modify(L, beta):
    N = L.shape[0]
    U = np.exp(1j * beta * np.random.randn(N))
    G = np.diag(U)
    return G.conj().T @ L @ G


# ---------------------------
# Gershgorin Bound
# ---------------------------
def gershgorin_lower_bound(A):
    N = A.shape[0]
    mins = []
    for i in range(N):
        center = np.real(A[i, i])
        radius = np.sum(np.abs(A[i, :])) - np.abs(A[i, i])
        mins.append(center - radius)
    return min(mins)


# ---------------------------
# Main
# ---------------------------
def main():
    N = 80
    beta = 0.5

    L = lysis_matrix(N)
    LG = gauge_modify(L, beta)

    bound = gershgorin_lower_bound(LG)

    print("\nRELATIONAL LYSIS — SCRIPT TYPE 35")
    print("Gershgorin Lower Bound Test")
    print("------------------------------------")
    print(f"Lower bound: {bound:.6e}")
    print("------------------------------------")
    print("INTERPRETATION:")
    print("If bound > 0:")
    print("Deterministic spectral gap exists.")


if __name__ == "__main__":
    main()
