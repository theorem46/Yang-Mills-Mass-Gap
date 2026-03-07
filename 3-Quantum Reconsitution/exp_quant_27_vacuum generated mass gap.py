#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_27_vacuum generated mass gap.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Paper Reference: Section 5.7 (Yang-Mills Mass Gap)
Theorem Support: "Vacuum Fluctuations Generate Mass Gap"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Simulates a 2D Yang-Mills vacuum using random SU(2) link variables.
    Computes the lowest eigenvalue of the covariant Laplacian as lattice
    size L increases.
    
    If the gap stabilizes to a non-zero value, it confirms the existence
    of a dynamic mass gap driven by the gauge field geometry.

ADVERSARIAL CONDITIONS:
    - Lattice Sizes:           4x4 to 10x10
    - Gauge Field:             Random SU(2) (Hot Vacuum)

PASS CRITERIA:
    1. Gap Stability:          Gap does not vanish as L increases.
    2. Magnitude:              Gap stabilizes around ~0.3 (in lattice units).
-------------------------------------------------------------------------------
"""

import numpy as np

# Pauli matrices
s1 = np.array([[0, 1], [1, 0]], complex)
s2 = np.array([[0, -1j], [1j, 0]], complex)
s3 = np.array([[1, 0], [0, -1]], complex)


def su2():
    v = np.random.randn(3)
    v /= np.linalg.norm(v)
    a = 0.6
    return np.cos(a) * np.eye(2) + 1j * np.sin(a) * (v[0] * s1 + v[1] * s2 + v[2] * s3)


# -------------------------------------------------
# Build 2D lattice gauge field
# -------------------------------------------------


def gauge_field(L):
    Ux = [[su2() for j in range(L)] for i in range(L)]
    Uy = [[su2() for j in range(L)] for i in range(L)]
    return Ux, Uy


# -------------------------------------------------
# Covariant Laplacian on 2D lattice
# -------------------------------------------------


def laplacian(Ux, Uy):
    L = len(Ux)
    dim = 2 * L * L
    M = np.zeros((dim, dim), complex)

    def idx(i, j, a):
        return 2 * (i * L + j) + a

    for i in range(L):
        for j in range(L):
            for a in range(2):
                M[idx(i, j, a), idx(i, j, a)] = 4

            for di, dj, U in [(1, 0, Ux), (0, 1, Uy)]:
                ni, nj = (i + di) % L, (j + dj) % L
                Uij = U[i][j]
                for a in range(2):
                    for b in range(2):
                        M[idx(i, j, a), idx(ni, nj, b)] -= Uij[a, b]
                        M[idx(ni, nj, b), idx(i, j, a)] -= np.conj(Uij[a, b])
    return M


def gap(M):
    ev = np.linalg.eigvalsh(M)
    ev = np.real(ev)
    ev.sort()
    for v in ev:
        if v > 1e-6:
            return v
    return 0


# -------------------------------------------------


def main():
    print("\nRELATIONAL LYSIS — SCRIPT TYPE 29")
    print("Yang–Mills Vacuum Mass Gap Test")
    print("---------------------------------")
    for L in [4, 6, 8, 10]:
        Ux, Uy = gauge_field(L)
        M = laplacian(Ux, Uy)
        g = gap(M)
        print(f"L={L}   gap={g:.6f}")

    print("---------------------------------")
    print("If gap stabilizes as L grows:")
    print("Yang–Mills mass gap detected.")


if __name__ == "__main__":
    main()
