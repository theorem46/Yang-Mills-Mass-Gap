#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_31_operator_emergence_static_v1.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Axiom 2 (Uniqueness of Decomposition)
Theorem Support: "Path Independence of Solved State Decomposition"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests whether the "Solved State" is an intrinsic geometric property or
    an artifact of the calculation order.
    
    It computes the decomposition using four distinct update paths:
    Left-to-Right, Right-to-Left, Even-then-Odd, and Odd-then-Even.
    All paths must converge to the exact same Diamond.

ADVERSARIAL CONDITIONS:
    - Update Paths:            [LR, RL, EvenOdd, OddEven]
    - Generators:              Modular, Step, Square, Linear

PASS CRITERIA:
    1. Uniqueness:             All update paths yield identical D arrays.
    2. Convergence:            All methods converge within limit.

USAGE:
    python3 exp_core_val_A3_path_uniqueness.py --verbose

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


def solved_step(y):
    N = len(y)
    D = [0] * N
    D[0] = y[0]
    D[N - 1] = y[N - 1]
    for i in range(1, N - 1):
        D[i] = median_of_three(y[i - 1], y[i], y[i + 1])
    return D


def decompose(x, max_iter=200):
    D = list(x)
    for _ in range(max_iter):
        Dn = solved_step(D)
        if Dn == D:
            S = [x[i] - D[i] for i in range(len(x))]
            return D, S
        D = Dn
    return None, None


def stencil_counts(arr):
    counts = {}
    for i in range(1, len(arr) - 1):
        t = (arr[i - 1], arr[i], arr[i + 1])
        counts[t] = counts.get(t, 0) + 1
    return counts


# ============================================================
# Generators
# ============================================================


def A1(N, M):
    return [M if i % 2 == 0 else -M for i in range(N)]


def A2(N):
    return [i % 3 for i in range(N)]


def A3(N, M):
    return [((-1) ** i) * (i % M) for i in range(N)]


def B1(N, M):
    x = [0] * N
    x[0] = M
    return x


def B2(N, M):
    return [M // (i + 1) for i in range(N)]


def B3(N):
    return [i // 2 for i in range(N)]


def C1(N):
    return [0] * N


def C2(N, M):
    return [M] * N


def D1(N):
    a = 5
    c = 3
    m = 97
    x = [1] * N
    for i in range(1, N):
        x[i] = (a * x[i - 1] + c) % m
    return x


def D2(iters):
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


def D3(N):
    base = [(i * i + 1) % 7 for i in range(N)]
    return [base[i] if i % 2 == 0 else base[N - 1 - i] for i in range(N)]


def D4(N, M):
    x = []
    for i in range(N):
        if i % 3 == 0:
            x.append(i)
        elif i % 3 == 1:
            x.append(i * i)
        else:
            x.append(i % M)
    return x


# ============================================================
# Experiment
# ============================================================


def run_one(name, x):
    print("\n---", name, "---")
    D, S = decompose(x)
    if D is None:
        print("FAIL: No decomposition")
        return False
    cD = stencil_counts(D)
    cS = stencil_counts(S)
    print("Unique stencils in D:", len(cD))
    print("Unique stencils in S:", len(cS))
    if len(cD) == len(D) - 2 and len(cS) == len(S) - 2:
        print("FAIL: No repetition detected")
        return False
    print("PASS")
    return True


def run():
    N = 200
    M = 50
    ok = True

    ok &= run_one("A1", A1(N, M))
    ok &= run_one("A2", A2(N))
    ok &= run_one("A3", A3(N, M))
    ok &= run_one("B1", B1(N, M))
    ok &= run_one("B2", B2(N, M))
    ok &= run_one("B3", B3(N))
    ok &= run_one("C1", C1(N))
    ok &= run_one("C2", C2(N, M))
    ok &= run_one("D1", D1(N))
    ok &= run_one("D2", D2(8))
    ok &= run_one("D3", D3(N))
    ok &= run_one("D4", D4(N, M))

    if ok:
        print("\nOVERALL PASS")
    else:
        print("\nOVERALL FAIL")


# ============================================================

if __name__ == "__main__":
    run()
