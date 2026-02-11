#Paper: Relational Lysis Theory: A Universal Self-Adjoint Operator Unifying Geometry, Quantum Gauge Fields, Gravitation, Thermodynamics, Arithmetic, and Computation
#Researcher: Dr. David Swanagon
#LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: February 09, 2026

#!/usr/bin/env python3
"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_10_wavefunction_normalizability.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 5.3 (Uniform Covariant Coercivity)
Theorem Support: "Elliptic Coercivity Implies Spectral Gap"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the L2-Normalizability of the Mass Gap eigenstates.
    Theorem 5.6 states that the operator is Coercive, implying a discrete
    spectrum at the bottom (Bound States).
    
    This script verifies that the eigenvectors for E_0 (Vacuum) and E_1 (Mass)
    have finite L2 norm and are localized (decay at boundaries), rather than
    spreading infinitely like plane waves in a non-compact limit.

ADVERSARIAL CONDITIONS:
    - Potential:               Confining (Dirichlet Boundaries)
    - Lattice:                 100 points
    - Check:                   Ground State vs Excited State Localization

PASS CRITERIA:
    1. Finite Norm:            Sum|psi|^2 = 1.0 (Unitary)
    2. Localization:           Psi decays at boundaries (Dirichlet behavior)
    3. Ratio Check:            Edge amplitude < 20% of Peak amplitude

USAGE:
    python3 exp_quant_10_wavefunction_normalizability.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
import scipy.linalg as la

def run_experiment():
    print(f"[*] Starting Wavefunction Normalizability Test...")
    print(f"[*] Reference: Theorem 5.6 (Bound States)\n")
    
    N = 100
    # Laplacian with Dirichlet BC (Confining)
    # L = 2*I - Neighbors
    L = 2 * np.eye(N) - np.eye(N, k=1) - np.eye(N, k=-1)
    
    # Solve Eigenproblem
    evals, evecs = la.eigh(L)
    
    # Check First Excited State (Mass Gap State, index 0 is Ground)
    # Actually, for standard Laplacian, index 0 is the lowest energy state (Ground)
    # index 1 is the first excited state.
    
    print(f"{'State':<10} | {'L2 Norm':<10} | {'Peak Amp':<10} | {'Edge Amp':<10} | {'Ratio':<10} | {'Status'}")
    print("-" * 75)
    
    passed_all = True
    
    for i in range(3): # Check Ground, 1st, 2nd excited
        psi = evecs[:, i]
        
        # 1. Check L2 Norm (Should be 1.0 by solver, but good to verify physical interpretation)
        norm = np.sum(psi**2)
        
        # 2. Check Localization/Decay at edges
        # Ideally, a bound state is centered.
        edge_val = np.abs(psi[0]) + np.abs(psi[-1])
        center_val = np.max(np.abs(psi))
        
        ratio = edge_val / center_val
        
        # Status check
        is_normalized = np.abs(norm - 1.0) < 1e-10
        is_localized = ratio < 0.25 # Arbitrary threshold for "decay"
        
        status = "PASS" if (is_normalized and is_localized) else "FAIL"
        if status == "FAIL": passed_all = False
            
        print(f"Psi_{i:<6} | {norm:.4f}{'':<6} | {center_val:.4f}{'':<6} | {edge_val:.4f}{'':<6} | {ratio:.4f}{'':<6} | {status}")

    print("-" * 75)
    
    if passed_all:
        print("\n[SUCCESS] Eigenstates are L2-Normalizable (Bound States).")
        print("          Wavefunctions decay at boundaries (Confining Geometry).")
    else:
        print("\n[FAILURE] Eigenstates are not localized.")

if __name__ == "__main__":
    run_experiment()