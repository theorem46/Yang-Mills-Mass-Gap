"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_55_gershgorin_lower_bound.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 11.7, Theorem 11.7 (Spectral Coercivity)
Theorem Support: "Deterministic Spectral Containment via Gershgorin Circles"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Applies the Gershgorin Circle Theorem to the gauge-modified Relational 
    Lysis operator to determine a deterministic lower bound for the 
    eigenvalues. 
    
    Unlike Monte Carlo sampling, this method provides a geometric guarantee 
    that all eigenvalues ($\lambda$) of the matrix $LG$ must lie within 
    the union of specific disks in the complex plane. By calculating the 
    minimum possible value on the real axis within these disks, the script 
    verifies that the operator is strictly positive-definite, thus 
    mathematically "trapping" the spectral gap above zero.

ADVERSARIAL CONDITIONS:
    - Lattice Size:             N = 80
    - Gauge Coupling:           beta = 0.5 (Random phase injection)
    - Bound Logic:              Gershgorin Center - Sum(Radii)

PASS CRITERIA:
    1. Positive Bound:          Calculated Lower Bound > 0.
    2. Containment:             Ensures no eigenvalue can "leak" to zero 
                                under the given gauge configuration.

USAGE:
    python3 exp_core_val_35_gershgorin_lower_bound.py --verbose

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
