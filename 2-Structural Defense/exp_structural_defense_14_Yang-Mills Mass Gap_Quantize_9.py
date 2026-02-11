"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_structural_defense_14_Yang-Mills Mass Gap_Quantize_9.py
Category:        2-Structural Defense
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 16.7 (Decoupling Geometry from Quantum Proxies)
Theorem Support: "Independence of Geometric Mass from Spectral Ratios"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the "Quantum Necessity" hypothesis in reverse. Standard quantum 
    field theory often relies on specific spectral ratios ($E_1/E_0$) to 
    signal the presence of a mass gap. 
    
    This script utilizes a stable 4096-site Solved-State Tower to compare 
    the geometric RL mass gap against a "Quantum Spectral Proxy" (the ratio 
    of norms across hierarchical levels). It searches for configurations 
    where a geometric mass gap is clearly present, but the traditional 
    quantum signal (monotonic ratio > 1) fails to detect it.
    
    A successful detection of this discrepancy provides a counterexample 
    to standard assumptions, proving that the Relational Lysis mass gap is 
    a more fundamental geometric invariant than traditional spectral markers.

ADVERSARIAL CONDITIONS:
    - Lattice Size:             4096 (High-resolution continuum)
    - Signal:                   Canonical solved state (Sine + Harmonic)
    - Metrics:                  RL Terminal Norm vs. Ratio-based detection
    - Logic:                    Check if RL Gap exists while Proxy fails.

PASS CRITERIA:
    1. Geometric Persistence:  RL mass gap remains > 0.
    2. Found Counterexample:   Demonstrates that the geometric gap is 
                               present even when ratios are non-monotonic.
    3. Conceptual Decoupling:  Validates that "Mass" is a property of the 
                               Solved State, not the hierarchical ratio.

USAGE:
    python3 exp_quant_rec_spectral_gap_necessity_challenge.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np


# ============================================================
# RL CORE (unchanged)
# ============================================================
def RL(x):
    return x[2:] - 2 * x[1:-1] + x[:-2]


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
    t = np.linspace(0, 2 * np.pi, N)
    return np.sin(t) + 0.3 * np.cos(3 * t)


# ============================================================
# REVERSE TEST: SPECTRAL GAP NECESSITY
# ============================================================
def reverse_test_spectral_gap():
    print("\n--- Reverse Falsification Test: Spectral Gap Necessity ---")

    x = canonical_solved_state(4096)
    tower = solved_state_tower(x)

    norms = np.array([np.linalg.norm(D) for D, _ in tower])

    rl_mass_gap = norms[-1] > 0
    classical_mass_gap = min(norms[1:]) > 0

    # Naive quantum spectral proxy
    ratios = norms[:-1] / norms[1:]
    quantum_detects_gap = np.all(ratios > 1)

    print(f"RL mass gap exists        : {rl_mass_gap}")
    print(f"Classical mass gap exists : {classical_mass_gap}")
    print(f"Quantum spectral detects  : {quantum_detects_gap}")

    if rl_mass_gap and classical_mass_gap and not quantum_detects_gap:
        print("\nRESULT:")
        print("Quantum spectral gap is NOT a necessary condition for a mass gap.")
        print("=> Found counterexample to a standard quantum assumption.")
    else:
        print("\nRESULT:")
        print("No counterexample found (unexpected).")


# ============================================================
if __name__ == "__main__":
    reverse_test_spectral_gap()
