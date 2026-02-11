"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_64_operator families.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 12.4, Unifying Theorem 3 (Operator Class Invariance)
Theorem Support: "Universality of Hierarchical Attractors for Self-Adjoint Operators"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the "Universality Hypothesis" across a diverse family of local 
    self-adjoint operators. The script evaluates four distinct operator 
    architectures:
    1. Standard 1D Laplacian (2nd Order)
    2. Fourth-Order Biharmonic ($\Delta^2$)
    3. Anisotropic Laplacian (Directional Bias)
    4. Variable-Coefficient Laplacian (Inhomogeneous Media)
    
    By evolving random states through these operators and extracting their 
    hierarchical Lysis signatures, the experiment determines if the 
    Relational Lysis hierarchy is sensitive to specific operator coefficients 
    or if it identifies a deeper, universal "Relational DNA" shared by all 
    local diffusion-like processes.

ADVERSARIAL CONDITIONS:
    - Lattice Size:             512 sites
    - Hierarchy Depth:         8 Levels
    - Evolution Steps:         6 (Near-steady state convergence)
    - Operator Variance:       Order (2nd/4th), Isotropy, Homogeneity
    - Metric:                   Cross-Operator Pairwise Cosine Similarity

PASS CRITERIA:
    1. Operator Invariance:    Mean |Cosine| between different operator 
                               families approaches 1.0.
    2. Structural Convergence: High-order and variable-coefficient operators 
                               map to the same fundamental attractor.

USAGE:
    python3 exp_core_val_local_operator_family_universality.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np

# -------------------------
# Utilities
# -------------------------


def normalize(v):
    n = np.linalg.norm(v)
    return v if n == 0 else v / n


def cosine(a, b):
    return float(np.dot(normalize(a), normalize(b)))


# -------------------------
# Relational Lysis
# -------------------------


def alignment_diamond(x):
    x = normalize(x)
    n = len(x)
    h = n // 2
    A = x[:h]
    B = x[h : 2 * h]
    d = normalize(np.array([np.sum(A), np.sum(B)]))
    recon = np.concatenate([np.full(h, d[0] / h), np.full(h, d[1] / h)])
    shadow = x[: 2 * h] - recon
    return d, shadow


def hierarchical_lysis(x, L):
    if L == 0:
        return normalize(x)
    d, s = alignment_diamond(x)
    return normalize(np.concatenate([d, hierarchical_lysis(s, L - 1)]))


# -------------------------
# Local Operators
# -------------------------


def laplacian(n):
    L = np.zeros((n, n))
    for i in range(n):
        L[i, i] = 2
        L[i, (i - 1) % n] = -1
        L[i, (i + 1) % n] = -1
    return L


def fourth_order(n):
    H = laplacian(n)
    return H @ H


def anisotropic_laplacian(n):
    L = np.zeros((n, n))
    for i in range(n):
        w1 = 1.0 + 0.5 * np.sin(i)
        w2 = 1.0 + 0.5 * np.cos(i)
        L[i, i] = w1 + w2
        L[i, (i - 1) % n] = -w1
        L[i, (i + 1) % n] = -w2
    return L


def variable_coeff_laplacian(n):
    c = np.random.rand(n)
    L = np.zeros((n, n))
    for i in range(n):
        L[i, i] = c[i] + c[(i + 1) % n]
        L[i, (i - 1) % n] = -c[i]
        L[i, (i + 1) % n] = -c[(i + 1) % n]
    return L


# -------------------------
# Main Test
# -------------------------


def run():
    N = 512
    DEPTH = 8
    STEPS = 6

    ops = {
        "laplacian": laplacian(N),
        "fourth_order": fourth_order(N),
        "anisotropic": anisotropic_laplacian(N),
        "variable_coeff": variable_coeff_laplacian(N),
    }

    attractors = {}

    print("\nRELATIONAL LYSIS — LOCAL OPERATOR FAMILY TEST")
    print("-" * 55)

    for name, H in ops.items():
        x = normalize(np.random.randn(N))
        for _ in range(STEPS):
            x = normalize(H @ x)
        v = hierarchical_lysis(x, DEPTH)
        attractors[name] = v
        print(f"{name} attractor norm: {np.linalg.norm(v):.6f}")

    print("\nPAIRWISE COSINES\n")

    names = list(attractors.keys())
    vals = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            c = cosine(attractors[names[i]], attractors[names[j]])
            vals.append(abs(c))
            print(f"{names[i]} vs {names[j]}: {c:.6f}")

    print("\nSUMMARY")
    print("Mean |cos|:", np.mean(vals))
    print("Min  |cos|:", np.min(vals))
    print("Max  |cos|:", np.max(vals))

    print(
        """
INTERPRETATION:
If Mean |cos| → 1 :
All local self-adjoint operators share same universal attractor.
"""
    )


if __name__ == "__main__":
    run()
