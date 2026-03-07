#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_structural_defense_18_Unifying Theorem 5_Correct.py
Category:        2-Structural Defense
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 12.5, Lemma 12.5 (Residual Persistence)
Theorem Support: "Non-Vanishing Property of the Shadow Energy Density"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the "Spectral Non-Collapse" hypothesis. In standard signal 
    processing, recursive projections often lead to a null residual. 
    Relational Lysis posits that for any nontrivial state evolved via a 
    local operator, the Shadow component is an essential geometric 
    feature that cannot be fully assimilated into the Alignment Diamond.
    
    The script evolves random noise through a 1D Laplacian to establish 
    local correlation and then measures the minimum Shadow energy across 
    an 8-level hierarchy. A strictly positive "Global min" shadow energy 
    proves that the hierarchy preserves the distinction between the 
    relational kernel and the high-frequency residual.

ADVERSARIAL CONDITIONS:
    - Lattice Size:             512 sites
    - Hierarchy Depth:         8 Levels
    - Evolution:               6 Steps of 1D Periodic Laplacian
    - Trials:                   20 Independent Stochastic initializations
    - Metric:                   Minimum $\ell_2$ norm of the Shadow across all levels

PASS CRITERIA:
    1. Energy Persistence:     Minimum shadow energy remains bounded away 
                               from zero (> 0) across all trials.
    2. Geometric Integrity:    Confirms that states do not "collapse" into 
                               a purely aligned, zero-residual state.

USAGE:
    python3 exp_top_val_spectral_non_collapse.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np


def normalize(v):
    return v / np.linalg.norm(v)


def alignment_diamond(x):
    x = normalize(x)
    n = len(x)
    h = n // 2
    A = x[:h]
    B = x[h : 2 * h]
    d = np.array([np.sum(A), np.sum(B)])
    d = normalize(d)
    recon = np.concatenate([np.full(h, d[0] / h), np.full(h, d[1] / h)])
    shadow = x[: 2 * h] - recon
    return d, shadow


def hierarchical_shadow_energy(x, depth):
    s = x
    energies = []
    for _ in range(depth):
        _, s = alignment_diamond(s)
        energies.append(np.linalg.norm(s))
    return energies


def laplacian(n):
    L = np.zeros((n, n))
    for i in range(n):
        L[i, i] = 2
        L[i, (i - 1) % n] = -1
        L[i, (i + 1) % n] = -1
    return L


def run():
    N = 512
    DEPTH = 8
    STEPS = 6
    trials = 20

    H = laplacian(N)

    mins = []

    for t in range(trials):
        x = normalize(np.random.randn(N))
        for _ in range(STEPS):
            x = normalize(H @ x)
        energies = hierarchical_shadow_energy(x, DEPTH)
        mins.append(min(energies))
        print(f"Trial {t}: min shadow = {min(energies):.6e}")

    print("\nSUMMARY")
    print("Global min:", min(mins))
    print("Global mean:", np.mean(mins))

    print(
        """
INTERPRETATION:
If minimum shadow remains > 0,
nontrivial states cannot collapse into alignment kernel.
"""
    )


if __name__ == "__main__":
    run()
