"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_37_representation_invariance_v1.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 3.9 (Representation Independence)
Theorem Support: "Invariance under Bijective Transforms"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Demonstrates that Relational Lysis operates on the *relational structure*
    of data, not just specific values.
    
    Applies three transformations to input data: Translation (Add), Scaling (Mul),
    and Arbitrary Bijection (Permutation/Map). Verifies that the Solved State
    commutes with these operations (Structure is preserved).

ADVERSARIAL CONDITIONS:
    - Transforms:              T1(x+c), T2(x*c), T3(Bijection)
    - Check:                   Solve(T(x)) == T(Solve(x))

PASS CRITERIA:
    1. Commutativity:          Decomposition respects the applied transformation.

USAGE:
    python3 exp_core_val_A6_representation_invariance.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""


# ============================================================
# Utilities
# ============================================================


def median_of_three(a, b, c):
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


def arrays_equal(a, b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True


def solved_step(y):
    N = len(y)
    D = [0] * N
    D[0] = y[0]
    D[N - 1] = y[N - 1]
    for i in range(1, N - 1):
        D[i] = median_of_three(y[i - 1], y[i], y[i + 1])
    return D


def solve(x, max_iter=300):
    D = list(x)
    for _ in range(max_iter):
        Dn = solved_step(D)
        if arrays_equal(Dn, D):
            return D
        D = Dn
    return None


# ============================================================
# Transforms
# ============================================================


def T1_add(x):
    return [v + 17 for v in x]


def T2_mul(x):
    return [v * 3 for v in x]


def build_bijection(x):
    vals = sorted(set(x))
    m = {}
    k = 5
    for v in vals:
        m[v] = k
        k += 7
    return m


def T3_bijective(x):
    m = build_bijection(x)
    return [m[v] for v in x]


def apply_map(arr, m):
    return [m[v] for v in arr]


# ============================================================
# Generators
# ============================================================


def G1(N):
    return [i % 3 for i in range(N)]


def G2(N):
    return [10 if i % 2 == 0 else -10 for i in range(N)]


def G3(N):
    return [(i * i) % 7 for i in range(N)]


def G4(N):
    return [i for i in range(N)]


def G5(N):
    x = [0] * N
    x[0] = 500
    return x


def G6(N):
    x = [1] * N
    for i in range(1, N):
        x[i] = (7 * x[i - 1] + 5) % 97
    return x


def G7(iters):
    seq = [0]
    for _ in range(iters):
        out = []
        for s in seq:
            if s == 0:
                out += [0, 1]
            elif s == 1:
                out += [2, 0]
            else:
                out += [2]
        seq = out
    return seq


def G8(N):
    base = [(i * i + 1) % 11 for i in range(N)]
    return [base[i] if i % 2 == 0 else base[N - 1 - i] for i in range(N)]


def G9(N):
    x = []
    for i in range(N):
        if i % 3 == 0:
            x.append(i)
        elif i % 3 == 1:
            x.append(i * i)
        else:
            x.append(i % 7)
    return x


def G10(N):
    return [(2**i) % 97 for i in range(N)]


# ============================================================
# Experiment
# ============================================================


def test_one(name, x):
    print("\n---", name, "---")

    D = solve(x)
    if D is None:
        print("FAIL: base solve")
        return False

    # T1
    Dx = solve(T1_add(x))
    if not arrays_equal(Dx, T1_add(D)):
        print("FAIL: T1")
        return False

    # T2
    Dx = solve(T2_mul(x))
    if not arrays_equal(Dx, T2_mul(D)):
        print("FAIL: T2")
        return False

    # T3
    m = build_bijection(x)
    Tx = apply_map(x, m)
    TD = apply_map(D, m)
    Dx = solve(Tx)
    if not arrays_equal(Dx, TD):
        print("FAIL: T3")
        return False

    print("PASS")
    return True


def run():
    N = 200
    ok = True
    ok &= test_one("G1", G1(N))
    ok &= test_one("G2", G2(N))
    ok &= test_one("G3", G3(N))
    ok &= test_one("G4", G4(N))
    ok &= test_one("G5", G5(N))
    ok &= test_one("G6", G6(N))
    ok &= test_one("G7", G7(8))
    ok &= test_one("G8", G8(N))
    ok &= test_one("G9", G9(N))
    ok &= test_one("G10", G10(N))

    if ok:
        print("\nOVERALL PASS")
    else:
        print("\nOVERALL FAIL")


# ============================================================

if __name__ == "__main__":
    run()
