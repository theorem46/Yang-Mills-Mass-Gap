"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_35_hierarchical_termination_v2.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Theorem 3.7 (Finite Termination)
Theorem Support: "Finite Termination of Hierarchical Lysis"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Validates that the recursive application of the decomposition (Hierarchical
    Lysis) does not lead to infinite regress.
    
    The script iteratively decomposes the Diamond D_k -> (D_k+1, S_k+1)
    and verifies that the system reaches a harmonic fixed point (L(D)=0)
    in a finite number of levels (Depth).

ADVERSARIAL CONDITIONS:
    - Generators:              Fractal, Cascading, recursive, and simple types
    - Depth Limit:             300 levels

PASS CRITERIA:
    1. Termination:            Fixed point reached within max depth.
    2. Stability:              Final state satisfies D_final = Solved_Step(D_final).

USAGE:
    python3 exp_core_val_A4_hierarchical_termination.py --verbose

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


def hierarchical_depth(x, max_depth=300):
    current = list(x)
    for k in range(1, max_depth + 1):
        D = solved_step(current)
        if arrays_equal(D, current):
            return k
        current = D
    return None


# ============================================================
# Generators
# ============================================================


# Simple
def S1(N):
    return [5] * N


def S2(N):
    return [i for i in range(N)]


# Generic
def G1(N):
    return [i % 3 for i in range(N)]


def G2(N):
    x = [1] * N
    for i in range(1, N):
        x[i] = (7 * x[i - 1] + 5) % 97
    return x


# Light-like
def L1(N):
    return [1000 if i % 2 == 0 else -1000 for i in range(N)]


# Singular
def N1(N):
    x = [0] * N
    x[0] = 1000
    return x


# Recursive
def R1(iters):
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


def R2(iters):
    seq = [0]
    for _ in range(iters):
        seq = seq + seq
    return seq


# Fractal
def F1(N):
    x = []
    for i in range(N):
        n = i
        ok = True
        while n > 0:
            if n % 3 == 1:
                ok = False
                break
            n //= 3
        x.append(0 if ok else 1)
    return x


def F2(N):
    x = []
    for i in range(N):
        v = i
        c = 0
        while v > 0:
            if v & 1:
                c += 1
            v //= 2
        x.append(c % 2)
    return x


# Cascading
def C1(N):
    x = [10, 9]
    for i in range(2, N):
        x.append(abs(x[i - 1] - x[i - 2]))
    return x


def C2(N):
    x = [1, 1]
    for i in range(2, N):
        a = i - x[i - 1]
        b = i - x[i - 2]
        if a < 0 or b < 0:
            x.append(1)
        else:
            x.append(x[a] + x[b])
    return x


# Extreme
def E1(N):
    x = []
    for i in range(N):
        x.append((2**i) % 997)
    return x


def E2(N):
    x = []
    f = 1
    for i in range(1, N + 1):
        f = (f * i) % 997
        x.append(f)
    return x


# ============================================================
# Experiment
# ============================================================


def run_one(name, x):
    print("\n---", name, "---")
    d = hierarchical_depth(x)
    if d is None:
        print("FAIL: No termination")
        return False
    print("Depth:", d)
    print("PASS")
    return True


def run():
    N = 200
    ok = True

    ok &= run_one("S1", S1(N))
    ok &= run_one("S2", S2(N))
    ok &= run_one("G1", G1(N))
    ok &= run_one("G2", G2(N))
    ok &= run_one("L1", L1(N))
    ok &= run_one("N1", N1(N))
    ok &= run_one("R1", R1(8))
    ok &= run_one("R2", R2(8))
    ok &= run_one("F1", F1(N))
    ok &= run_one("F2", F2(N))
    ok &= run_one("C1", C1(N))
    ok &= run_one("C2", C2(N))
    ok &= run_one("E1", E1(N))
    ok &= run_one("E2", E2(N))

    if ok:
        print("\nOVERALL PASS")
    else:
        print("\nOVERALL FAIL")


# ============================================================

if __name__ == "__main__":
    run()
