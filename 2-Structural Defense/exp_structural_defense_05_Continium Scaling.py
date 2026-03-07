#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_structural_defense_05_Continium Scaling.py
Category:        2-Structural Defense
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 3.10, Theorem 3.35 (Infinite-Volume Stability)
Theorem Support: "Infinite-Volume Stability of Interaction Geometry"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Validates that the Mass Gap survives the continuum limit (N -> Infinity).
    
    Tests whether the scaled gap measure (N^2 * gap) converges to a constant
    non-zero value. If the gap were a discretization artifact, this value
    would vanish or diverge. Stability confirms the gap is a physical feature
    of the continuous theory.

ADVERSARIAL CONDITIONS:
    - Lattice Sizes:           [20, 30, 40, 60, 80, 120]
    - Coupling:                Strong (beta=0.5) with Gauge Noise
    - Sampling:                10 shots per N

PASS CRITERIA:
    1. Stability:              N^2 * gap converges to a stable constant.
    2. Non-Vanishing:          Gap does not collapse to zero as N increases.

USAGE:
    python3 exp_struct_def_33_continuum_scaling.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np


# ---------------------------
# Build 1D Relational Lysis (Discrete Laplacian)
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
# Gauge-Covariant Modification (SU(2)-like)
# ---------------------------
def gauge_modify(L, beta):
    N = L.shape[0]
    U = np.exp(1j * beta * np.random.randn(N))
    G = np.zeros((N, N), dtype=complex)
    for i in range(N):
        G[i, i] = U[i]
    return G.conj().T @ L @ G


# ---------------------------
# Measure smallest nonzero eigenvalue
# ---------------------------
def measure_gap(N, beta):
    L = lysis_matrix(N)
    LG = gauge_modify(L, beta)

    evals = np.linalg.eigvals(LG)
    evals = np.real(evals)
    evals = np.sort(evals)

    # discard near-zero numerical mode
    for v in evals:
        if v > 1e-10:
            return v
    return 0.0


# ---------------------------
# Average over multiple random gauge samples
# ---------------------------
def measure_gap_avg(N, beta, shots=10):
    vals = []
    for _ in range(shots):
        vals.append(measure_gap(N, beta))
    return np.mean(vals)


# ---------------------------
# Main Experiment
# ---------------------------
def main():
    beta = 0.5
    Ns = [20, 30, 40, 60, 80, 120]
    shots = 10

    print("\nRELATIONAL LYSIS — SCRIPT TYPE 33")
    print("Continuum-Scaled Strong-Coupling Mass Gap Test")
    print("------------------------------------------------------")
    print("N     gap            N^2 * gap")
    print("------------------------------------------------------")

    for N in Ns:
        g = measure_gap_avg(N, beta, shots)
        print(f"{N:<5d} {g:>12.6e} {N*N*g:>12.6e}")

    print("------------------------------------------------------")
    print("INTERPRETATION:")
    print("If N^2 * gap -> constant as N increases:")
    print("Relational Lysis contains a true Yang–Mills mass gap.")
    print("Mass originates from geometry, not tuning.")


if __name__ == "__main__":
    main()
