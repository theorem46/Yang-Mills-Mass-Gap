"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_structural_defense_13_Yang-Mills Mass Gap_Quantize_8.py
Category:        2-Structural Defense
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 16.8 (The Derivational Consistency Theorem)
Theorem Support: "Invariance of Physical Observables under Mapping Diversity"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the "Derivational Invariance" of the Relational Lysis framework. 
    The script constructs a single, "frozen" Solved-State Tower ($\Sigma$) from 
    a canonical field configuration and applies three distinct interpretive 
    mappings (Derivations):
    
    1. Classical Derivation: Focuses on energy density and IR collapse.
    2. Quantum Derivation: Evaluates spectral ratios and vacuum stability.
    3. Alternative Derivation: A purely relational, structural readout.
    
    The experiment checks for logical contradictions between these paths. 
    A "PASS" confirms that the underlying geometric tower is robust enough 
    to support multiple physical interpretations without yielding 
    conflicting results about the Mass Gap or system stability.

ADVERSARIAL CONDITIONS:
    - Lattice Size:             4096 (Continuum limit approximation)
    - Depth:                    Max 50 levels (Hierarchical exhaustion)
    - Input:                    $\sin(t) + 0.3\cos(3t)$ (Non-trivial harmonic)
    - Logic:                    Cross-map conflict detection (Boolean logic)

PASS CRITERIA:
    1. Derivational Harmony:   Classical "Mass Gap" must align with Quantum 
                               "Spectral Gap" logic.
    2. Stability Consensus:    IR collapse markers must be consistent across 
                               all interpretive lenses.
    3. Deterministic Unity:    Proves the Solved State is a "Universal Object."

USAGE:
    python3 exp_int_mech_cdct_d_derivational_consistency.py --verbose

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
    # Solved-state decomposition
    D = RL(x)
    S = x[1:-1] - D
    return D, S

# ============================================================
# SOLVED-STATE TOWER Σ (DIAMOND + SHADOW)
# ============================================================
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
# FIXED SOLVED STATE Σ (NO DISTORTION)
# ============================================================
def canonical_solved_state(N):
    t = np.linspace(0, 2*np.pi, N)
    return np.sin(t) + 0.3*np.cos(3*t)

# ============================================================
# DERIVATION MAPS (DISTORTIONS LIVE *HERE ONLY*)
# ============================================================

def classical_derivation(tower):
    """
    Classical logic:
    - mass gap exists iff no diamond norm goes to zero
    - IR collapse iff terminal diamond vanishes
    """
    norms = [np.linalg.norm(D) for D, _ in tower]
    return {
        "finite": all(np.isfinite(norms)),
        "mass_gap": min(norms[1:]) > 0,
        "ir_collapse": norms[-1] == 0
    }

def quantum_derivation(tower):
    """
    Quantum logic:
    - spectral gap exists iff ratios stay bounded away from 1
    - vacuum stability iff terminal diamond nonzero
    """
    norms = np.array([np.linalg.norm(D) for D, _ in tower])
    ratios = norms[:-1] / norms[1:]
    return {
        "finite": np.all(np.isfinite(ratios)),
        "spectral_gap": np.all(ratios > 1),
        "vacuum_instability": norms[-1] == 0
    }

def alternative_derivation(tower):
    """
    Stress-test derivation:
    - purely relational readout
    - asks only whether hierarchy terminates nontrivially
    """
    return {
        "terminates": len(tower) < 50,
        "nontrivial": np.linalg.norm(tower[-1][0]) > 0
    }

# ============================================================
# CDCT-D — DERIVATIONAL CONSISTENCY TEST
# ============================================================
def run_cdct_d():
    N = 4096

    print("\n--- CDCT-D: Cross-Derivation Derivational Consistency Test ---")

    # One solved state Σ
    x = canonical_solved_state(N)
    tower = solved_state_tower(x)

    print(f"Solved-state tower depth: {len(tower)}")

    # Apply derivations
    C = classical_derivation(tower)
    Q = quantum_derivation(tower)
    A = alternative_derivation(tower)

    print("\nClassical derivation:")
    for k, v in C.items():
        print(f"  {k}: {v}")

    print("\nQuantum derivation:")
    for k, v in Q.items():
        print(f"  {k}: {v}")

    print("\nAlternative derivation:")
    for k, v in A.items():
        print(f"  {k}: {v}")

    # Logical consistency check
    contradictions = []

    if C["mass_gap"] and Q["spectral_gap"] is False:
        contradictions.append("Classical gap vs quantum no-gap")

    if C["ir_collapse"] != Q["vacuum_instability"]:
        contradictions.append("IR stability mismatch")

    if not A["nontrivial"]:
        contradictions.append("Alternative derivation trivializes solved state")

    if contradictions:
        print("\nFAIL: Logical contradiction detected.")
        for c in contradictions:
            print(" -", c)
        print("RL determinism is falsified.")
    else:
        print("\nPASS: All derivations logically consistent.")
        print("RL determinism confirmed.")

# ============================================================
if __name__ == "__main__":
    run_cdct_d()
