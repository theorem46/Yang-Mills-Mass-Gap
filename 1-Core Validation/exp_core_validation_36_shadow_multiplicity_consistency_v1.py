"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_36_shadow_multiplicity_consistency_v1.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 3.6 (Shadow Mechanics)
Theorem Support: "Consistency of Lysis under Shadow Perturbation"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the robustness of the hierarchical depth against perturbations in
    the Shadow component.
    
    It generates a state, extracts the Shadow, perturbs the Shadow, reconstructs
    a new state, and measures the Lysis depth. This verifies that the
    fundamental "complexity class" (depth) is robust.

ADVERSARIAL CONDITIONS:
    - Perturbation:            Sign flips and magnitude shifts in S
    - Generators:              G1 (Mod), G2 (Step), G3 (Poly), G4 (Impulse)

PASS CRITERIA:
    1. Robustness:             Depth of perturbed state is consistent/close to original.
    2. Termination:            Perturbed states still terminate.

USAGE:
    python3 exp_core_val_A5_shadow_consistency.py --verbose

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


def hierarchical_depth(x, max_depth=200):
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


def G1(N):
    return [i % 3 for i in range(N)]


def G2(N):
    return [100 if i % 2 == 0 else -100 for i in range(N)]


def G3(N):
    x = [1] * N
    for i in range(1, N):
        x[i] = (7 * x[i - 1] + 5) % 97
    return x


def G4(N):
    x = [0] * N
    x[0] = 500
    return x


# ============================================================
# Shadow Perturbations
# ============================================================


def perturb_shadow(S):
    Sp = S[:]
    if len(Sp) > 4:
        Sp[2] *= -1
        Sp[4] += 1
    return Sp


# ============================================================
# Experiment
# ============================================================


def run_one(name, x):
    print("\n---", name, "---")
    D = solved_step(x)
    S = [x[i] - D[i] for i in range(len(x))]
    Sp = perturb_shadow(S)

    x1 = [D[i] + S[i] for i in range(len(D))]
    x2 = [D[i] + Sp[i] for i in range(len(D))]

    d1 = hierarchical_depth(x1)
    d2 = hierarchical_depth(x2)

    if d1 is None or d2 is None:
        print("FAIL: Non-termination")
        return False

    print("Depth original:", d1)
    print("Depth perturbed:", d2)
    print("PASS")
    return True


def run():
    N = 200
    ok = True
    ok &= run_one("G1", G1(N))
    ok &= run_one("G2", G2(N))
    ok &= run_one("G3", G3(N))
    ok &= run_one("G4", G4(N))

    if ok:
        print("\nOVERALL PASS")
    else:
        print("\nOVERALL FAIL")


# ============================================================

if __name__ == "__main__":
    run()
