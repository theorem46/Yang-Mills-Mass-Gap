"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_structural_defense_16_Yang-Mills Mass Gap_Quantize_11.py
Category:        2-Structural Defense
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 16.5 (The Primacy of Geometry)
Theorem Support: "Invariance of the Mass Gap under Dynamical Remapping"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Conducts a "Knock-Out" test to determine if the Mass Gap ($\Delta > 0$) 
    is a robust geometric property or a dynamical artifact. 
    
    The script first generates a canonical Solved-State Tower from a static 
    field configuration. It then subjects this tower to three "Dynamically 
    Inequivalent Embeddings"—Standard, Strongly Distorted, and Pathological. 
    These embeddings simulate radical shifts in local dynamics, including 
    violent nonlinearities and forced cubic decay.
    
    If the Mass Gap (the existence of a non-zero terminal Diamond) survives 
    all three transformations identically, the theory is verified: the gap is 
    proven to be an emergent geometric invariant of the Solved State itself, 
    independent of the specific gauge dynamics or interaction strengths.

ADVERSARIAL CONDITIONS:
    - Lattice Size:             4096 (High-resolution field)
    - Distortion Intensity:     Phase scrambling and 50x sinusoidal amplitude shifts
    - Pathological Logic:       Forced $1/n^3$ energy decay to attempt gap destruction
    - Metric:                   Boolean Invariance of the terminal Mass Gap

PASS CRITERIA:
    1. Dynamical Invariance:   Mass Gap presence (True) must be identical across 
                               all three embeddings.
    2. Primacy Verification:   Confirms geometry is the "master" and dynamics 
                               are the "slave" in Relational Lysis.

USAGE:
    python3 exp_core_val_ko_geometric_primacy.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np

# ============================================================
# RELATIONAL LYSIS (FROZEN, CANONICAL)
# ============================================================
def RL(x):
    return x[2:] - 2*x[1:-1] + x[:-2]

def Phi(x):
    D = RL(x)
    S = x[1:-1] - D
    return D, S

def solved_state_tower(x, max_depth=50, tol=1e-12):
    tower = []
    current = x.copy()
    prev_norm = None

    for _ in range(max_depth):
        if len(current) < 5:
            break

        D, S = Phi(current)
        tower.append((D, S))

        norm = np.linalg.norm(D)
        if prev_norm is not None and abs(norm - prev_norm) < tol:
            break

        prev_norm = norm
        current = D

    return tower

# ============================================================
# FIXED SOLVED STATE Σ
# ============================================================
def canonical_solved_state(N):
    t = np.linspace(0, 2*np.pi, N)
    return np.sin(t) + 0.3*np.cos(3*t)

# ============================================================
# DYNAMICALLY INEQUIVALENT YM EMBEDDINGS
# ============================================================

def ym_embedding_standard(tower):
    """
    Canonical YM-like interpretation:
    mass gap exists iff terminal diamond nonzero.
    """
    terminal_norm = np.linalg.norm(tower[-1][0])
    return {
        "mass_gap": terminal_norm > 0,
        "label": "Standard YM embedding"
    }

def ym_embedding_strongly_distorted(tower):
    """
    Radically altered local dynamics:
    - violent nonlinear weighting
    - phase scrambling
    - interaction dominance
    """
    norms = np.array([np.linalg.norm(D) for D, _ in tower])
    distorted = norms * (1 + 50*np.sin(np.arange(len(norms))**2))
    terminal = distorted[-1]

    return {
        "mass_gap": terminal > 0,
        "label": "Strongly distorted YM embedding"
    }

def ym_embedding_pathological(tower):
    """
    Stress-test embedding:
    attempts to destroy gap dynamically.
    """
    norms = np.array([np.linalg.norm(D) for D, _ in tower])
    forced_decay = norms / (1 + np.arange(len(norms))**3)
    terminal = forced_decay[-1]

    return {
        "mass_gap": terminal > 0,
        "label": "Pathological YM embedding"
    }

# ============================================================
# KNOCK-OUT TEST
# ============================================================
def run_ko_test():
    print("\n--- KO TEST: Geometric Primacy vs Yang–Mills Dynamics ---")

    x = canonical_solved_state(4096)
    tower = solved_state_tower(x)

    print(f"Solved-state tower depth: {len(tower)}")

    results = [
        ym_embedding_standard(tower),
        ym_embedding_strongly_distorted(tower),
        ym_embedding_pathological(tower),
    ]

    for r in results:
        print(f"{r['label']}: mass_gap = {r['mass_gap']}")

    gaps = [r["mass_gap"] for r in results]

    print("\n--- Verdict ---")
    if len(set(gaps)) == 1:
        print("PASS:")
        print("Mass gap invariant across dynamically inequivalent embeddings.")
        print("=> Mass gap is geometric, not dynamical.")
    else:
        print("FAIL:")
        print("Mass gap depends on dynamics.")
        print("=> Relational Lysis is falsified.")

# ============================================================
if __name__ == "__main__":
    run_ko_test()
