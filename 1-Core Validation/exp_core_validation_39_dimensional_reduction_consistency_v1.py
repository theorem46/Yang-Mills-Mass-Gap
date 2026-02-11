"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_39_dimensional_reduction_consistency_v1.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 3.10 (Dimensional Reduction)
Theorem Support: "Admissibility of Dimensionally Collapsed States"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the consistency of the theory across dimensions.
    It takes a 2D generator, "collapses" it to 1D via row-wise medians,
    and then verifies that this collapsed 1D state is still a valid
    Relational Lysis state (admits a solved state and finite hierarchy).

ADVERSARIAL CONDITIONS:
    - Input:                   2D Grids (40x40)
    - Collapse Op:             Row Median
    - Check:                   1D Hierarchical Termination

PASS CRITERIA:
    1. Admissibility:          Collapsed vector admits a valid decomposition.
    2. Termination:            Collapsed vector has finite Lysis depth.

USAGE:
    python3 exp_core_val_A8_dimensional_collapse.py --verbose

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


def arrays_equal(a, b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True


# ============================================================
# 1D Solved + Hierarchy
# ============================================================


def median3(a, b, c):
    if a <= b:
        if b <= c:
            return b
        elif a <= c:
            return c
        else:
            return a
    else:
        if a <= c:
            return a
        elif b <= c:
            return c
        else:
            return b


def solved_step_1d(x):
    N = len(x)
    D = [0] * N
    D[0] = x[0]
    D[N - 1] = x[N - 1]
    for i in range(1, N - 1):
        D[i] = median3(x[i - 1], x[i], x[i + 1])
    return D


def solve_1d(x, max_iter=300):
    cur = list(x)
    for _ in range(max_iter):
        D = solved_step_1d(cur)
        if arrays_equal(D, cur):
            return D
        cur = D
    return None


def hierarchical_depth_1d(x, max_depth=300):
    cur = list(x)
    for k in range(1, max_depth + 1):
        D = solved_step_1d(cur)
        if arrays_equal(D, cur):
            return k
        cur = D
    return None


# ============================================================
# Collapse
# ============================================================


def collapse_rows(G):
    return [median_list(row) for row in G]


# ============================================================
# Generators (2D)
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
    v = collapse_rows(G)
    D = solve_1d(v)
    if D is None:
        print("FAIL: no solved-state")
        return False
    d = hierarchical_depth_1d(v)
    if d is None:
        print("FAIL: no hierarchical termination")
        return False
    print("Depth:", d)
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
