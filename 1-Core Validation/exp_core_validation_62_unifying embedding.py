"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_62_unifying embedding.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 12.2, Unifying Theorem 2 (Hierarchical Embedding)
Theorem Support: "Stochastic Stability of Recursive Hierarchical Embeddings"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Validates the convergence of a Hierarchical Lysis cascade when applied to 
    an operator-evolved state (1D Laplacian). 
    
    The script initializes random noise, evolves it through several steps of 
    a 1D periodic Laplacian (H), and then applies recursive hierarchical 
    decomposition. The "state = diamond + shadow" logic is applied iteratively 
    to the shadow, building a deep structural signature. 
    
    By comparing the final signatures (finals) across different random seeds, 
    the experiment determines if the operator's intrinsic relational 
    geometry forces the hierarchy into a singular, universal attractor state, 
    regardless of the initial entropy.

ADVERSARIAL CONDITIONS:
    - Dimensions:              512 (Lattice sites)
    - Hierarchy Depth:         8 Levels
    - Evolution Steps:         6 (Operator applications)
    - Seed Variance:           5 Independent Gaussian initializations
    - Metric:                   Pairwise Cosine Similarity of final embeddings

PASS CRITERIA:
    1. Convergence:            Mean |Cosine| between seeds → 1.0.
    2. Topological Stability:  Consistent hierarchical signatures across seeds.

USAGE:
    python3 exp_core_val_unifying_theorem_type_2_embedding.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np

# ============================================================
# Utilities
# ============================================================


def normalize(v):
    n = np.linalg.norm(v)
    if n == 0:
        return v
    return v / n


def cosine(a, b):
    return float(np.dot(normalize(a), normalize(b)))


# ============================================================
# Alignment Diamond + Shadow
# ============================================================


def alignment_diamond(x):
    """
    Maps state -> (diamond, shadow)
    Diamond = 2D alignment signature
    Shadow  = residual after reconstruction
    """
    x = normalize(x)
    n = len(x)
    half = n // 2

    A = x[:half]
    B = x[half : 2 * half]

    d0 = np.sum(A)
    d1 = np.sum(B)
    diamond = normalize(np.array([d0, d1]))

    recon = np.concatenate(
        [np.full(half, diamond[0] / half), np.full(half, diamond[1] / half)]
    )

    shadow = x[: 2 * half] - recon
    return diamond, shadow


# ============================================================
# Recursive Hierarchical Relational Lysis
# ============================================================


def hierarchical_lysis(x, depth):
    """
    state = diamond + shadow
    shadow recursively decomposed
    """
    if depth == 0:
        return normalize(x)

    d, s = alignment_diamond(x)
    sub = hierarchical_lysis(s, depth - 1)

    return normalize(np.concatenate([d, sub]))


# ============================================================
# Operator (1D Laplacian)
# ============================================================


def laplacian(n):
    L = np.zeros((n, n))
    for i in range(n):
        L[i, i] = 2
        L[i, (i - 1) % n] = -1
        L[i, (i + 1) % n] = -1
    return L


# ============================================================
# Main Experiment
# ============================================================


def run():
    DIM = 512
    DEPTH = 8
    STEPS = 6
    SEEDS = 5

    H = laplacian(DIM)
    finals = []

    print("\nRELATIONAL LYSIS — UNIFYING THEOREM TYPE 2")
    print("Hierarchical Operator Embedding Test")
    print("-" * 60)

    for k in range(SEEDS):
        x = np.random.randn(DIM)
        x = normalize(x)

        for _ in range(STEPS):
            x = normalize(H @ x)

        f = hierarchical_lysis(x, DEPTH)
        finals.append(f)

        print(f"Seed {k} final norm: {np.linalg.norm(f):.6f}")

    print("\nPAIRWISE COSINES BETWEEN FINAL STATES\n")

    vals = []
    for i in range(SEEDS):
        for j in range(i + 1, SEEDS):
            c = cosine(finals[i], finals[j])
            vals.append(abs(c))
            print(f"{i}-{j}: {c:.6f}")

    print("\nSUMMARY")
    print("Mean |cos|:", np.mean(vals))
    print("Min  |cos|:", np.min(vals))
    print("Max  |cos|:", np.max(vals))

    print(
        """
INTERPRETATION:
If mean |cos| → 1 :
Universal hierarchical alignment attractor exists.
"""
    )


# ============================================================

if __name__ == "__main__":
    run()
