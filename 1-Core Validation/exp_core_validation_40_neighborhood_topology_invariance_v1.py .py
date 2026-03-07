#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_40_neighborhood_topology_invariance_v1.py .py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 4.1 (Geometric Universality)
Theorem Support: "Invariance across Neighborhood Topologies"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Verifies that the concept of a "Solved State" is robust to changes in the
    definition of "locality" (Neighborhood Topology).
    
    Compares convergence under Von Neumann (4-neighbor) and Moore (8-neighbor)
    topologies on 2D grids. The existence of a solved state should not depend
    critically on the specific neighbor count.

ADVERSARIAL CONDITIONS:
    - Topologies:              Von Neumann vs Moore
    - Generators:              Various 2D structures

PASS CRITERIA:
    1. Universality:           Both topologies yield valid solved states.

USAGE:
    python3 exp_core_val_A9_topology_invariance.py --verbose

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
    for i in range(len(A)):
        for j in range(len(A[0])):
            if A[i][j] != B[i][j]:
                return False
    return True


# ============================================================
# Solvers
# ============================================================


def solved_step_vn(G):
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


def solved_step_moore(G):
    n = len(G)
    m = len(G[0])
    D = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if i == 0 or j == 0 or i == n - 1 or j == m - 1:
                D[i][j] = G[i][j]
            else:
                vals = []
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        vals.append(G[i + di][j + dj])
                D[i][j] = median_list(vals)
    return D


def solve(G, step, max_iter=400):
    cur = [row[:] for row in G]
    for _ in range(max_iter):
        D = step(cur)
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


def G13(n, m):
    cx = n // 2
    cy = m // 2
    return [[max(abs(i - cx), abs(j - cy)) for j in range(m)] for i in range(n)]


# ============================================================
# Experiment
# ============================================================


def run_one(name, G):
    print("\n---", name, "---")
    D1 = solve(G, solved_step_vn)
    if D1 is None:
        print("FAIL: VN")
        return False
    D2 = solve(G, solved_step_moore)
    if D2 is None:
        print("FAIL: Moore")
        return False
    print("PASS")
    return True


def run():
    n = 40
    m = 40
    ok = True
    ok &= run_one("G1", G1(n, m))
    ok &= run_one("G2", G2(n, m))
    ok &= run_one("G3", G3(n, m))
    ok &= run_one("G5", G5(n, m))
    ok &= run_one("G6", G6(n, m))
    ok &= run_one("G7", G7(n, m))
    ok &= run_one("G8", G8(n, m))
    ok &= run_one("G9", G9(n, m))
    ok &= run_one("G10", G10(n, m))
    ok &= run_one("G13", G13(n, m))

    if ok:
        print("\nOVERALL PASS")
    else:
        print("\nOVERALL FAIL")


# ============================================================

if __name__ == "__main__":
    run()
