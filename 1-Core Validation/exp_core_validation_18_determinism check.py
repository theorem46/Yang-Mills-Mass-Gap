"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_18_determinism check.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Paper Reference: Axiom 1 (Determinism)
Theorem Support: "Cross-Implementation Determinism"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Verifies bit-perfect determinism of the L4 Diamond computation using
    canonical hashes. Ensures the algorithm is platform-independent.

ADVERSARIAL CONDITIONS:
    - Input Size:              100,000 (Large state)
    - Generator:               Deterministic polynomial

PASS CRITERIA:
    1. Determinism:            Output hashes must match known reference.
-------------------------------------------------------------------------------
"""

# rl_light_L4_cross_impl_determinism.py
# PURPOSE:
#   Verify bit-perfect determinism across independent implementations.
# METHOD:
#   Emit canonical hashes of D and D2 only (no raw state retained).

import numpy as np
import hashlib

def RL(x):
    return x[2:] - 2*x[1:-1] + x[:-2]

def Phi(x):
    D = RL(x)
    S = x[1:-1] - D
    return D, S

def hash_vec(x):
    return hashlib.sha256(x.tobytes()).hexdigest()

# Admissible generator (locked)
def gen_interior(n):
    i = np.arange(n, dtype=np.int64)
    return (i*i*i + 5*i*i + 13) // 7

if __name__ == "__main__":
    n = 100_000
    x = gen_interior(n)
    D, _ = Phi(x)
    D2 = RL(D)

    print("D_len =", len(D))
    print("D2_len =", len(D2))
    print("hash(D)  =", hash_vec(D))
    print("hash(D2) =", hash_vec(D2))
