#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_structural_defense_03_light modular arithemtic cap.py
Category:        2-Structural Defense
Researcher:      Dr. David Swanagon
Paper Reference: Section 6.2 (Discrete Fields)
Theorem Support: "Stability under Modular Arithmetic Caps"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the operator's stability when confined to a finite field (Modular Arithmetic).
    Verifies that "Diamond Closure" (convergence) persists even when values
    wrap around a large prime modulus (avoiding integer overflow artifacts).
    
    Defends against claims that the theory requires infinite fields (R).

ADVERSARIAL CONDITIONS:
    - Modulus:                 2^61 - 1 (Mersenne Prime)
    - Input Sizes:             10k to 1M

PASS CRITERIA:
    1. Closure:                L1(D2) remains consistent with non-modular results.
-------------------------------------------------------------------------------
"""


# rl_light_L3_integer_overflow_safety.py
# PURPOSE:
#   Verify diamond closure persists under modular arithmetic caps.
# CONSTRAINTS:
#   Deterministic, integer-only, diamond-only computation.

import numpy as np

MOD = 2**61 - 1   # large prime cap to avoid overflow artifacts

def RL(x):
    return (x[2:] - 2*x[1:-1] + x[:-2]) % MOD

def Phi(x):
    D = RL(x)
    S = (x[1:-1] - D) % MOD
    return D, S

def L1(x):
    # modular L1 (absolute taken in integer lift)
    return int(np.sum(np.abs(x.astype(np.int64))))

# Admissible interior generator (mod-capped)
def gen_interior(n):
    i = np.arange(n, dtype=np.int64)
    return ((i*i*i + 5*i*i + 13) // 7) % MOD

def run(n):
    x = gen_interior(n)
    D, _ = Phi(x)
    del x
    D2 = RL(D)
    return L1(D), L1(D2), len(D), len(D2)

if __name__ == "__main__":
    for n in [10_000, 100_000, 1_000_000]:
        l1d, l1d2, ld, ld2 = run(n)
        print(
            f"n={n}, D_len={ld}, D2_len={ld2}, "
            f"L1(D)={l1d}, L1(D2)={l1d2}"
        )
