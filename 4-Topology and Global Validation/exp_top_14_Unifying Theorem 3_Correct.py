"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_top_14_Unifying Theorem 3_Correct.py
Category:        4-Topology and Global Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 33.4 (Attractor Dynamics in Lysis Space)
Theorem Support: "Asymptotic Alignment of Hierarchical Diamonds"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Evaluates the "Attractor Strength" of the Relational Lysis hierarchy. 
    In emergent systems, a stable logic is defined by its ability to pull 
    diverse initial conditions toward a common geometric solution (the gap). 
    
    The script first establishes a 'Geometric Attractor' ($v^*$) by evolving 
    a random field. It then conducts multiple trials with new random seeds, 
    evolving them through the same Laplacian and Lysis depth. 
    
    By measuring the ratio of the component parallel to the attractor versus 
     the orthogonal component ($Parallel/Orthogonal$), the script determines if 
    the system successfully separates the 'Massive' kernel from the 'Shadow' 
    noise. A high ratio indicates that the hierarchy is a robust classifier of 
    physical states.

ADVERSARIAL CONDITIONS:
    - Lattice Resolution:      512 Units
    - Lysis Depth (L):         8 Levels
    - Evolution Steps:         6 Laplacian iterations
    - Trials:                  10 Independent stochastic seeds
    - Metric:                   Parallel/Orthogonal Projection Ratio

PASS CRITERIA:
    1. Attractor Stability:    Trial ratios must be significantly $> 1$.
    2. Geometric Coherence:    Independent random starts must align with $v^*$.
    3. Emergent Logic:         Confirms the gap is a topological destination, 
                               not a random fluctuation.

USAGE:
    python3 exp_neu_em_kernel_gap_separation_attractor.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np

# ---------------------------
# Utilities
# ---------------------------


def normalize(v):
    n = np.linalg.norm(v)
    return v if n == 0 else v / n


def cosine(a, b):
    return float(np.dot(normalize(a), normalize(b)))


# ---------------------------
# Lysis
# ---------------------------


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


# ---------------------------
# Operator
# ---------------------------


def laplacian(n):
    L = np.zeros((n, n))
    for i in range(n):
        L[i, i] = 2
        L[i, (i - 1) % n] = -1
        L[i, (i + 1) % n] = -1
    return L


# ---------------------------
# Main
# ---------------------------


def run():
    N = 512
    DEPTH = 8
    STEPS = 6
    TRIALS = 10

    H = laplacian(N)

    # build attractor
    x = normalize(np.random.randn(N))
    for _ in range(STEPS):
        x = normalize(H @ x)
    vstar = hierarchical_lysis(x, DEPTH)

    print("\nEstimated attractor norm:", np.linalg.norm(vstar))

    ratios = []

    for k in range(TRIALS):
        y = normalize(np.random.randn(N))
        for _ in range(STEPS):
            y = normalize(H @ y)
        y = hierarchical_lysis(y, DEPTH)

        proj = np.dot(y, vstar)
        parallel = abs(proj)
        orth = np.sqrt(max(0, 1 - proj**2))
        ratios.append(parallel / orth)

        print(
            f"Trial {k}: parallel={parallel:.6f} orth={orth:.6f} ratio={parallel/orth:.2f}"
        )

    print("\nMean ratio:", np.mean(ratios))

    print(
        """
INTERPRETATION:
Large ratio >> 1 implies kernel/gap separation.
"""
    )


if __name__ == "__main__":
    run()
