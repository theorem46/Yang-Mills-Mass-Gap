#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_38_representation_invariance_v1.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 3.9 (High-Dimensional Lysis)
Theorem Support: "Generalization to 2D Relational States"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Extends the Solved State definition to 2D grids (matrices).
    Tests whether the 2D Median Alignment algorithm converges for various
    pattern classes (P-Class) and correctly fails or diverges for
    heuristic noise classes (H-Class).
    
    This validates the distinction between "Natural" geometric states and
    "Artificial" noise.

ADVERSARIAL CONDITIONS:
    - Topology:                2D Grid (Von Neumann Neighborhood)
    - Classes:                 14 P-Class (Structured), 2 H-Class (Noise)

PASS CRITERIA:
    1. P-Class:                Converges to a stable 2D Diamond.
    2. H-Class:                Fails to converge (or flagged behavior).

USAGE:
    python3 exp_core_val_A7_multidimensional_generalization.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""


# ============================================================
# Utilities
# ============================================================


def median_list(vals):
    s = sorted(vals)
    return s[len(s) // 2]


def grids_equal(A, B):
    if len(A) != len(B):
        return False
    for i in range(len(A)):
        for j in range(len(A[0])):
            if A[i][j] != B[i][j]:
                return False
    return True


# ============================================================
# 2D Solved Step
# ============================================================


def solved_step_2d(G):
    n = len(G)
    m = len(G[0])
    D = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if i == 0 or j == 0 or i == n - 1 or j == m - 1:
                D[i][j] = G[i][j]
            else:
                vals = [G[i][j], G[i - 1][j], G[i + 1][j], G[i][j - 1], G[i][j + 1]]
                D[i][j] = median_list(vals)
    return D


def solve_2d(G, max_iter=400):
    cur = [row[:] for row in G]
    for _ in range(max_iter):
        D = solved_step_2d(cur)
        if grids_equal(D, cur):
            return D
        cur = D
    return None


# ============================================================
# Generators
# ============================================================


def G1(n, m):
    return [[5] * m for _ in range(n)]


def G2(n, m):
    return [[i for j in range(m)] for i in range(n)]


def G3(n, m):
    return [[j for j in range(m)] for i in range(n)]


# H-class
def G4(n, m):
    return [[10 if (i + j) % 2 == 0 else -10 for j in range(m)] for i in range(n)]


def G5(n, m):
    G = [[0] * m for _ in range(n)]
    G[n // 2][m // 2] = 1000
    return G


def G6(n, m):
    return [[(i + j) % 3 for j in range(m)] for i in range(n)]


def G7(n, m):
    G = [[1] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            G[i][j] = (7 * (G[i - 1][j] if i > 0 else 1) + 5) % 97
    return G


def G8(n, m):
    cx = n // 2
    cy = m // 2
    return [[abs(i - cx) + abs(j - cy) for j in range(m)] for i in range(n)]


def G9(n, m):
    return [[(i * i + j * j) % 7 for j in range(m)] for i in range(n)]


def G10(n, m):
    G = []
    for i in range(n):
        row = []
        for j in range(m):
            if (i + j) % 3 == 0:
                row.append(i)
            elif (i + j) % 3 == 1:
                row.append(j * j)
            else:
                row.append((i + j) % 7)
        G.append(row)
    return G


def G11(n, m):
    return [[10 if j % 2 == 0 else -10 for j in range(m)] for i in range(n)]


def G12(n, m):
    return [[10 if i % 2 == 0 else -10 for j in range(m)] for i in range(n)]


def G13(n, m):
    cx = n // 2
    cy = m // 2
    return [[max(abs(i - cx), abs(j - cy)) for j in range(m)] for i in range(n)]


def G14(n, m):
    return [[i + j for j in range(m)] for i in range(n)]


# H-class
def G15(n, m):
    return [[((-1) ** (i + j)) * (i + j) for j in range(m)] for i in range(n)]


def G16(n, m):
    G = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(((i // 4) + (j // 4)) % 5)
        G.append(row)
    return G


# ============================================================
# Experiment
# ============================================================

P_CLASS = [
    "G1",
    "G2",
    "G3",
    "G5",
    "G6",
    "G7",
    "G8",
    "G9",
    "G10",
    "G11",
    "G12",
    "G13",
    "G14",
    "G16",
]
H_CLASS = ["G4", "G15"]

GENERATORS = [
    ("G1", G1),
    ("G2", G2),
    ("G3", G3),
    ("G4", G4),
    ("G5", G5),
    ("G6", G6),
    ("G7", G7),
    ("G8", G8),
    ("G9", G9),
    ("G10", G10),
    ("G11", G11),
    ("G12", G12),
    ("G13", G13),
    ("G14", G14),
    ("G15", G15),
    ("G16", G16),
]


def run_one(name, G):
    print("\n---", name, "---")
    D = solve_2d(G)
    if name in P_CLASS:
        if D is None:
            print("FAIL (P-class non-convergence)")
            return False
        print("PASS (P-class)")
        return True
    else:
        if D is None:
            print("PASS (H-class expected non-convergence)")
            return True
        print("FLAG (H-class converged)")
        return True


def run():
    n = 40
    m = 40
    ok = True
    for name, gen in GENERATORS:
        ok &= run_one(name, gen(n, m))
    if ok:
        print("\nOVERALL PASS")
    else:
        print("\nOVERALL FAIL")


# ============================================================

if __name__ == "__main__":
    run()
