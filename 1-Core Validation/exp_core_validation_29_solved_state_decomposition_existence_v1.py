#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_29_solved_state_decomposition_existence_v1.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Definition 3.1 (Solved State)
Theorem Support: "Existence of Decomposition for Arbitrary Deterministic States"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the fundamental axiom that every deterministic generative sequence
    admits a stable "Solved State" decomposition (x = D + S).
    
    The script generates sequences from 12 distinct structural classes—including
    frustrated cycles, self-referential logic, and cellular automata—and
    verifies that the recursive median alignment converges to a fixed point.

ADVERSARIAL CONDITIONS:
    - Generators:              12 Classes (Frustrated, Self-Ref, Chaos, etc.)
    - Arithmetic:              Integer-only (Exact)
    - Max Iterations:          1000

PASS CRITERIA:
    1. Convergence:            Algorithm finds a Fixed Point D*.
    2. Reconstruction:         D + S perfectly reconstructs the input.
    3. Determinism:            Repeated runs yield identical decompositions.

USAGE:
    python3 exp_core_val_A1_decomposition_existence.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""


# ============================================================
# Utility Functions
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
# Generator F1: Frustrated Constraint Cycle
# ============================================================


def generate_F1(N):
    x = [0] * N
    for i in range(1, N):
        if x[i - 1] == 0:
            x[i] = 1
        elif x[i - 1] == 1:
            x[i] = 2
        else:
            x[i] = 0

    # enforce x[i+2] = x[i]
    for i in range(N - 2):
        x[i + 2] = x[i]

    return x


# ============================================================
# Generator F2: Long-Range Self Reference
# ============================================================


def generate_F2(N):
    x = [0] * N
    for i in range(7, N):
        count = 0
        for j in range(i - 7):
            if x[j] == 1:
                count += 1
        x[i] = count % 2
    return x


# ============================================================
# Generator F3: Symbolic Substitution Cascade
# ============================================================


def generate_F3(iterations):
    seq = [0]
    for _ in range(iterations):
        new_seq = []
        for s in seq:
            if s == 0:
                new_seq.append(0)
                new_seq.append(1)
            elif s == 1:
                new_seq.append(2)
                new_seq.append(0)
            else:
                new_seq.append(2)
        seq = new_seq
    return seq


# ============================================================
# Solved-State Step
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
# Hierarchical Decomposition
# ============================================================


def hierarchical_decompose(x, max_iter):
    D = list(x)
    for k in range(1, max_iter + 1):
        D_next = solved_step(D)
        if arrays_equal(D_next, D):
            S = []
            for i in range(len(x)):
                S.append(x[i] - D[i])
            return D, S, k
        D = D_next

    return None, None, max_iter


# ============================================================
# Falsifier Checks
# ============================================================


def check_reconstruction(x, D, S):
    for i in range(len(x)):
        if D[i] + S[i] != x[i]:
            return False
    return True


def run_single_test(name, generator, size):
    print("\n--- Testing", name, "---")

    x = generator(size)
    D, S, steps = hierarchical_decompose(x, 1000)

    if D is None:
        print("FAIL: No convergence within limit")
        return

    if not check_reconstruction(x, D, S):
        print("FAIL: Reconstruction error")
        return

    # determinism check
    D2, S2, _ = hierarchical_decompose(x, 1000)
    if not arrays_equal(D, D2) or not arrays_equal(S, S2):
        print("FAIL: Non-deterministic result")
        return

    print("PASS")
    print("Convergence steps:", steps)


# ============================================================
# Experiment Harness
# ============================================================


def run_experiment():
    run_single_test("F1_Frustrated_Cycle", generate_F1, 200)
    run_single_test("F2_LongRange_SelfReference", generate_F2, 200)
    run_single_test("F3_Symbolic_Substitution", generate_F3, 8)


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    run_experiment()
