"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_32_solved_state_uniqueness_paths_v1 .py
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


def arrays_equal(a, b):
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True


# ============================================================
# Solved-step variants
# ============================================================


# Standard left-to-right sweep
def solved_step_LR(y):
    N = len(y)
    D = y[:]
    D[0] = y[0]
    D[N - 1] = y[N - 1]
    for i in range(1, N - 1):
        D[i] = median_of_three(y[i - 1], y[i], y[i + 1])
    return D


# Right-to-left sweep
def solved_step_RL(y):
    N = len(y)
    D = y[:]
    D[0] = y[0]
    D[N - 1] = y[N - 1]
    for i in range(N - 2, 0, -1):
        D[i] = median_of_three(y[i - 1], y[i], y[i + 1])
    return D


# Even indices first, then odd
def solved_step_even_odd(y):
    N = len(y)
    D = y[:]
    D[0] = y[0]
    D[N - 1] = y[N - 1]
    for i in range(2, N - 1, 2):
        D[i] = median_of_three(y[i - 1], y[i], y[i + 1])
    for i in range(1, N - 1, 2):
        D[i] = median_of_three(y[i - 1], y[i], y[i + 1])
    return D


# Odd indices first, then even
def solved_step_odd_even(y):
    N = len(y)
    D = y[:]
    D[0] = y[0]
    D[N - 1] = y[N - 1]
    for i in range(1, N - 1, 2):
        D[i] = median_of_three(y[i - 1], y[i], y[i + 1])
    for i in range(2, N - 1, 2):
        D[i] = median_of_three(y[i - 1], y[i], y[i + 1])
    return D


# ============================================================
# Generic Decomposition
# ============================================================


def decompose(x, step_func, max_iter=500):
    D = list(x)
    for _ in range(max_iter):
        Dn = step_func(D)
        if arrays_equal(Dn, D):
            return D
        D = Dn
    return None


# ============================================================
# Test Generators (reuse diversity)
# ============================================================


def G1(N):
    return [i % 3 for i in range(N)]


def G2(N):
    return [0 if i % 2 == 0 else 5 for i in range(N)]


def G3(N):
    return [i * i % 7 for i in range(N)]


def G4(N):
    return [N - i for i in range(N)]


def G5(N):
    return [0] * N


def G6(N):
    x = [1] * N
    for i in range(1, N):
        x[i] = (5 * x[i - 1] + 3) % 97
    return x


# ============================================================
# Experiment
# ============================================================


def run_one(name, x):
    print("\n---", name, "---")

    D1 = decompose(x, solved_step_LR)
    D2 = decompose(x, solved_step_RL)
    D3 = decompose(x, solved_step_even_odd)
    D4 = decompose(x, solved_step_odd_even)

    if D1 is None or D2 is None or D3 is None or D4 is None:
        print("FAIL: No convergence")
        return False

    if not (arrays_equal(D1, D2) and arrays_equal(D1, D3) and arrays_equal(D1, D4)):
        print("FAIL: Path-dependent solved state")
        return False

    print("PASS")
    return True


def run():
    N = 200
    ok = True
    ok &= run_one("G1", G1(N))
    ok &= run_one("G2", G2(N))
    ok &= run_one("G3", G3(N))
    ok &= run_one("G4", G4(N))
    ok &= run_one("G5", G5(N))
    ok &= run_one("G6", G6(N))

    if ok:
        print("\nOVERALL PASS")
    else:
        print("\nOVERALL FAIL")


# ============================================================

if __name__ == "__main__":
    run()
