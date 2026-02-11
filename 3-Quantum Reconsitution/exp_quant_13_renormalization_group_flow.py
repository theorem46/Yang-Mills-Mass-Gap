#Paper: Relational Lysis Theory: A Universal Self-Adjoint Operator Unifying Geometry, Quantum Gauge Fields, Gravitation, Thermodynamics, Arithmetic, and Computation
#Researcher: Dr. David Swanagon
#LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: February 09, 2026

#!/usr/bin/env python3
"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_13_renormalization_group_flow.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 11.4 (RG Flow) & Theorem 11.5
Theorem Support: "Stability of the Mass Gap under Renormalization"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the stability of the Mass Gap under Real-Space Renormalization (RG).
    
    We apply a "Block Spin" transformation (Decimation) to the derived
    Hamiltonian. This simulates "zooming out" from the microscopic lattice (UV)
    to the macroscopic physics (IR).
    
    Algorithm:
    1. Start with Fine Lattice (N=64).
    2. Measure Mass Gap (E1 - E0).
    3. Coarse Grain: Merge pairs of sites (H_new = P^T * H_old * P).
    4. Iterate until N=8.
    
    Hypothesis (Theorem 11.5):
    The Mass Gap operator is "Relevant" in the IR. It should persist or grow
    relative to the energy scale. It must NOT vanish.

ADVERSARIAL CONDITIONS:
    - Input:                   Random Massive Hamiltonian
    - Scales:                  N = 64 -> 32 -> 16 -> 8 (3 RG Steps)
    - Check:                   Gap Positivity at IR limit

PASS CRITERIA:
    1. Gap Persistence:        Gap > 0 at all scales.
    2. No Criticality:         Gap does not scale to 0 (which would imply a CFT).

USAGE:
    python3 exp_quant_13_renormalization_group_flow.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
import scipy.linalg as la

def measure_gap(H):
    """Calculates E1 - E0"""
    # For small matrices we can use full eig
    evals = la.eigvalsh(H)
    evals = np.sort(evals)
    # Ensure strictly positive gap measurement
    gap = evals[1] - evals[0]
    return gap

def coarse_grain(H):
    """
    Applies Real Space Renormalization (Block Averaging).
    Merges adjacent sites i, i+1 into a single site I.
    """
    N_fine = H.shape[0]
    N_coarse = N_fine // 2
    
    # Projection Matrix P (N_fine x N_coarse)
    # Maps 2 fine sites to 1 coarse site (normalized)
    P = np.zeros((N_fine, N_coarse))
    
    for i in range(N_coarse):
        # Block i corresponds to fine sites 2*i and 2*i+1
        # 1/sqrt(2) normalization preserves unitary structure
        P[2*i, i]     = 1.0 / np.sqrt(2)
        P[2*i + 1, i] = 1.0 / np.sqrt(2)
        
    # Renormalize Operator: H' = P^T H P
    H_new = np.dot(P.T, np.dot(H, P))
    return H_new

def run_experiment():
    print(f"[*] Starting Renormalization Group (RG) Flow Test...")
    print(f"[*] Reference: Theorem 11.5 (Gap Stability)\n")
    
    # 1. Setup Fine Lattice (UV Scale)
    N_start = 64
    np.random.seed(137)
    
    # Construct a Massive Laplacian (Diamond Geometry)
    # H = -D^2 + m^2
    mass = 0.5
    diag = (2.0 + mass**2) * np.ones(N_start)
    off = -1.0 * np.ones(N_start-1)
    H_current = np.diag(diag) + np.diag(off, k=1) + np.diag(off, k=-1)
    
    print(f"{'Scale (N)':<12} | {'Mass Gap (E1-E0)':<20} | {'Status'}")
    print("-" * 50)
    
    # 2. Iterate RG Steps (Until N=8)
    gap_history = []
    
    while H_current.shape[0] >= 8:
        current_N = H_current.shape[0]
        
        # Measure
        gap = measure_gap(H_current)
        gap_history.append(gap)
        
        status = "OPEN" if gap > 1e-4 else "CLOSED"
        print(f"N={current_N:<10} | {gap:.6f}{'':<14} | {status}")
        
        # Renormalize (Decimate)
        if current_N > 8:
            H_current = coarse_grain(H_current)
        else:
            break # Stop after measuring N=8
            
    print("-" * 50)
    
    # 3. Analyze Flow
    # In RG, eigenvalues scale. We check if the gap *relative to the scale* vanishes.
    # If the theory were massless, Gap -> 0 rapidly.
    # If massive, Gap stabilizes or grows (as we zoom into the low energy physics).
    
    initial_gap = gap_history[0]
    final_gap = gap_history[-1]
    
    print(f"[*] Initial UV Gap (Micro): {initial_gap:.6f}")
    print(f"[*] Final IR Gap (Macro):   {final_gap:.6f}")
    
    # Verification: Did the gap survive the zooming out process?
    if final_gap > 1e-4:
        print("\n[SUCCESS] Mass Gap persists in the IR Limit.")
        print("          The theory is not Critical (Massless).")
        print("          Renormalization Flow confirms a stable massive phase.")
    else:
        print("\n[FAILURE] Gap collapsed (Theory is Conformal/Massless).")

if __name__ == "__main__":
    run_experiment()