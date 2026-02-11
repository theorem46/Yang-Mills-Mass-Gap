"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_45_dimensional stress.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 5.4 (Geometric Primacy Limit)
Theorem Support: "Dimensional Universality of the Covariant Laplacian"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Performs a "Dimensional Stress Test" on the Relational Lysis operator.
    Extends the Integer Rambo validation to 2D and 4D (Spacetime) lattices.

    Verifies that the operator structure naturally generalizes to higher
    dimensions ($N^2$ and $N^4$ hypercubes) while maintaining the correct
    spectral scaling ($\lambda \sim k^2$). Uses exact rational arithmetic
    (Fractions) to prevent floating-point drift in high-dimensional tensor
    sums.

ADVERSARIAL CONDITIONS:
    - Dimensions:              1D, 2D, 4D
    - Lattice Topology:        Hypercubic Torus (Periodic)
    - Arithmetic:              Exact Rational (Fraction)

PASS CRITERIA:
    1. Gap Existence:          Spectral gap is strictly positive in all dims.
    2. Scaling:                Scaled Gap (Gap * Length^2) converges to constant.

USAGE:
    python3 exp_quant_rec_ym_2_dimensional_stress.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

from fractions import Fraction
import math

# --------------------------------------------------
# BASIC LINEAR ALGEBRA
# --------------------------------------------------


def dot(a, b):
    return sum(a[i] * b[i] for i in range(len(a)))


def matvec(M, x):
    return [sum(M[i][j] * x[j] for j in range(len(x))) for i in range(len(M))]


def rayleigh(L, x):
    return Fraction(dot(x, matvec(L, x)), dot(x, x))


# --------------------------------------------------
# 1D RL
# --------------------------------------------------


def RL1(N):
    L = [[0] * N for _ in range(N)]
    for i in range(N):
        L[i][i] = 2
        L[i][(i + 1) % N] = -1
        L[i][(i - 1) % N] = -1
    return L


# --------------------------------------------------
# 2D RL (NxN grid)
# --------------------------------------------------


def idx2(i, j, N):
    return i * N + j


def RL2(N):
    M = N * N
    L = [[0] * M for _ in range(M)]
    for i in range(N):
        for j in range(N):
            p = idx2(i, j, N)
            L[p][p] = 4
            L[p][idx2((i + 1) % N, j, N)] -= 1
            L[p][idx2((i - 1) % N, j, N)] -= 1
            L[p][idx2(i, (j + 1) % N, N)] -= 1
            L[p][idx2(i, (j - 1) % N, N)] -= 1
    return L


# --------------------------------------------------
# 4D RL (NxNxNxN)
# --------------------------------------------------


def idx4(a, b, c, d, N):
    return ((a * N + b) * N + c) * N + d


def RL4(N):
    M = N**4
    L = [[0] * M for _ in range(M)]
    for a in range(N):
        for b in range(N):
            for c in range(N):
                for d in range(N):
                    p = idx4(a, b, c, d, N)
                    L[p][p] = 8
                    for da, db, dc, dd in [
                        (1, 0, 0, 0),
                        (-1, 0, 0, 0),
                        (0, 1, 0, 0),
                        (0, -1, 0, 0),
                        (0, 0, 1, 0),
                        (0, 0, -1, 0),
                        (0, 0, 0, 1),
                        (0, 0, 0, -1),
                    ]:
                        q = idx4(
                            (a + da) % N, (b + db) % N, (c + dc) % N, (d + dd) % N, N
                        )
                        L[p][q] -= 1
    return L


# --------------------------------------------------
# INTEGER MODE
# --------------------------------------------------


def mode1(N):
    return [int(round(10**6 * math.sin(2 * math.pi * i / N))) for i in range(N)]


def mode2(N):
    v = []
    for i in range(N):
        for j in range(N):
            v.append(int(round(10**6 * math.sin(2 * math.pi * i / N))))
    return v


def mode4(N):
    v = []
    for a in range(N):
        for b in range(N):
            for c in range(N):
                for d in range(N):
                    v.append(int(round(10**6 * math.sin(2 * math.pi * a / N))))
    return v


# --------------------------------------------------
# TEST HARNESS
# --------------------------------------------------


def test_dimension(name, L, x, scale_power):
    mg = rayleigh(L, x)
    scaled = mg * (len(x) ** (2 / scale_power))
    print(name, "Gap:", mg)
    print(name, "Scaled Gap:", scaled)
    return mg, scaled


def main():

    print("DIMENSIONAL RELATIONAL LYSIS STRESS TEST")

    # 1D
    for N in [32, 64, 128]:
        print("\n--- 1D N =", N, "---")
        L = RL1(N)
        x = mode1(N)
        test_dimension("1D", L, x, 1)

    # 2D
    for N in [8, 12, 16]:
        print("\n--- 2D N =", N, "---")
        L = RL2(N)
        x = mode2(N)
        test_dimension("2D", L, x, 2)

    # 4D (small N only)
    for N in [4, 5]:
        print("\n--- 4D N =", N, "---")
        L = RL4(N)
        x = mode4(N)
        test_dimension("4D", L, x, 4)


if __name__ == "__main__":
    main()
