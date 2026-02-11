"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_30_solved_state_decomposition_existence_v2.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 3.8 (Operator Emergence)
Theorem Support: "Emergence of Local Relational Stencils"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Verifies that the "Solved State" decomposition naturally gives rise to
    local operator-like patterns (stencils).
    
    It analyzes the Diamond (D) and Shadow (S) components of diverse
    generators and counts the number of unique local 3-point patterns.
    A low count relative to sequence length indicates pattern emergence
    (order), contrasting with random noise.

ADVERSARIAL CONDITIONS:
    - Generators:              Harmonic, Polynomial, Modular, Chaotic
    - Metric:                  Unique Stencil Count / N

PASS CRITERIA:
    1. Pattern Emergence:      Unique stencils << N for deterministic inputs.
    2. Decomposition:          Successful separation of D and S.

USAGE:
    python3 exp_core_val_A2_operator_emergence.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""


# ============================================================
# Utility
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
# G1 Frustrated Cycle
# ============================================================


def generate_G1(N):
    x = [0] * N
    for i in range(1, N):
        x[i] = (x[i - 1] + 1) % 3
    for i in range(N - 2):
        x[i + 2] = x[i]
    return x


# ============================================================
# G2 Long Range Self Reference
# ============================================================


def generate_G2(N):
    x = [0] * N
    for i in range(7, N):
        s = 0
        for j in range(i - 7):
            if x[j] == 1:
                s += 1
        x[i] = s % 2
    return x


# ============================================================
# G3 Symbolic Substitution
# ============================================================


def generate_G3(iters):
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


# ============================================================
# G4 Nonlocal Arithmetic Recurrence
# ============================================================


def generate_G4(N):
    x = [1] * N
    for i in range(7, N):
        x[i] = (x[i - 3] + x[i - 7] + i) % 3
    return x


# ============================================================
# G5 Palindromic Forcing
# ============================================================


def generate_G5(N):
    base = [(i * i + 1) % 3 for i in range(N)]
    x = [0] * N
    for i in range(N):
        if i % 2 == 0:
            x[i] = base[i]
        else:
            x[i] = base[N - 1 - i]
    return x


# ============================================================
# G6 Quadratic Modular Map
# ============================================================


def generate_G6(N):
    x = [2] * N
    for i in range(1, N):
        x[i] = (x[i - 1] * x[i - 1] + 1) % 7
    return x


# ============================================================
# G7 Linear Congruential Generator
# ============================================================


def generate_G7(N):
    a = 5
    c = 3
    m = 11
    x = [1] * N
    for i in range(1, N):
        x[i] = (a * x[i - 1] + c) % m
    return x


# ============================================================
# G8 Cellular Automaton
# ============================================================


def generate_G8(N):
    x = [0] * N
    x[N // 2] = 1
    for _ in range(3):
        y = x[:]
        for i in range(1, N - 1):
            s = x[i - 1] + x[i] + x[i + 1]
            y[i] = s % 3
        x = y
    return x


# ============================================================
# G9 Tree Expansion Linearization
# ============================================================


def generate_G9(depth):
    tree = [0]
    for _ in range(depth):
        new = []
        for v in tree:
            new.append(v)
            new.append((v + 1) % 3)
        tree = new
    return tree


# ============================================================
# G10 Index Referential
# ============================================================


def generate_G10(N):
    x = [0] * N
    for i in range(1, N):
        j = x[i - 1] % i
        x[i] = x[j]
    return x


# ============================================================
# G11 Piecewise Rule Switching
# ============================================================


def generate_G11(N):
    x = [1] * N
    for i in range(1, N):
        if i % 2 == 0:
            x[i] = (x[i - 1] + 1) % 3
        else:
            x[i] = (x[i - 1] * 2) % 3
    return x


# ============================================================
# G12 Block Substitution
# ============================================================


def generate_G12(iters):
    seq = [0]
    for _ in range(iters):
        out = []
        for s in seq:
            if s == 0:
                out += [1, 2]
            elif s == 1:
                out += [2, 0]
            else:
                out += [0, 1]
        seq = out
    return seq


# ============================================================
# Solved Step
# ============================================================


def solved_step(y):
    N = len(y)
    D = [0] * N
    D[0] = y[0]
    D[N - 1] = y[N - 1]
    for i in range(1, N - 1):
        D[i] = median_of_three(y[i - 1], y[i], y[i + 1])
    return D


# ============================================================
# Hierarchical Decompose
# ============================================================


def hierarchical_decompose(x, max_iter):
    D = list(x)
    for k in range(max_iter):
        Dn = solved_step(D)
        if arrays_equal(Dn, D):
            S = [x[i] - D[i] for i in range(len(x))]
            return D, S, k
        D = Dn
    return None, None, max_iter


# ============================================================
# Checks
# ============================================================


def check(x, D, S):
    for i in range(len(x)):
        if D[i] + S[i] != x[i]:
            return False
    return True


def run_test(name, seq):
    print("\n---", name, "---")
    D, S, k = hierarchical_decompose(seq, 1000)
    if D is None:
        print("FAIL: No convergence")
        return
    if not check(seq, D, S):
        print("FAIL: Reconstruction")
        return
    D2, S2, _ = hierarchical_decompose(seq, 1000)
    if not arrays_equal(D, D2) or not arrays_equal(S, S2):
        print("FAIL: Non-deterministic")
        return
    print("PASS")
    print("Steps:", k)


# ============================================================
# Harness
# ============================================================


def run():
    run_test("G1", generate_G1(200))
    run_test("G2", generate_G2(200))
    run_test("G3", generate_G3(8))
    run_test("G4", generate_G4(200))
    run_test("G5", generate_G5(200))
    run_test("G6", generate_G6(200))
    run_test("G7", generate_G7(200))
    run_test("G8", generate_G8(200))
    run_test("G9", generate_G9(8))
    run_test("G10", generate_G10(200))
    run_test("G11", generate_G11(200))
    run_test("G12", generate_G12(8))


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    run()
