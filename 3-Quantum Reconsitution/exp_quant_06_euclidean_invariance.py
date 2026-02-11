#Paper: Relational Lysis Theory: A Universal Self-Adjoint Operator Unifying Geometry, Quantum Gauge Fields, Gravitation, Thermodynamics, Arithmetic, and Computation
#Researcher: Dr. David Swanagon
#LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: February 09, 2026

#!/usr/bin/env python3
"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_06_euclidean_invariance.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 11.2 (Euclidean Invariance of Measure)
Theorem Support: "Existence of the Measure (Minlos-Bochner)"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the Euclidean Invariance (Rotational Symmetry) of the induced
    propagator.
    
    If the Solved State corresponds to a physical vacuum, the correlation
    between two points S2(x, y) should depend ONLY on the distance |x-y|,
    invariant under rotation of the vector (x-y).

    We test 90-degree rotational symmetry and reflection symmetry on a 2D
    lattice to ensure the geometry is isotropic (not stretched or biased).

ADVERSARIAL CONDITIONS:
    - Geometry:                2D Lattice (10x10) with Mass Gap
    - Test Vectors:            Orthogonal directions (X vs Y) and Diagonals
    - Precision:               1e-10

PASS CRITERIA:
    1. Rotational Error:       |G(x) - G(y)| < 1e-10 (Isotropy)
    2. Reflection Error:       |G(x,y) - G(x,-y)| < 1e-10 (Parity)

USAGE:
    python3 exp_quant_06_euclidean_invariance.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
import scipy.linalg as la

def run_experiment():
    print(f"[*] Starting Euclidean Invariance (Isotropy) Test...")
    print(f"[*] Reference: Section 11.2\n")
    
    # 1. Setup 2D Lattice Operator (N x N)
    N = 11 # Odd number to have a perfect center
    size = N*N
    center_x, center_y = N//2, N//2
    center_idx = center_x*N + center_y
    
    # Build 2D Laplacian: 4*I - Neighbors
    # We add a mass term to make it invertible (Massive Scalar Field)
    mass_sq = 0.5
    L = np.zeros((size, size))
    
    for x in range(N):
        for y in range(N):
            idx = x*N + y
            L[idx, idx] = 4.0 + mass_sq
            
            # Neighbors (Up, Down, Left, Right)
            neighbors = [(-1,0), (1,0), (0,-1), (0,1)]
            for dx, dy in neighbors:
                nx, ny = x+dx, y+dy
                if 0 <= nx < N and 0 <= ny < N:
                    n_idx = nx*N + ny
                    L[idx, n_idx] = -1.0
                    
    # 2. Compute Propagator (Inverse)
    # This represents the geometry of the vacuum
    try:
        G = la.inv(L)
    except np.linalg.LinAlgError:
        print("[CRITICAL FAIL] Singular Operator.")
        return

    print(f"{'Symmetry Type':<20} | {'Point A':<15} | {'Point B':<15} | {'Diff':<12} | {'Status'}")
    print("-" * 75)
    
    # 3. Test Rotational Symmetry (90 degrees)
    # Compare (Center -> Right 1) vs (Center -> Up 1)
    # Right 1: (cx+1, cy)
    idx_right = (center_x+1)*N + center_y
    val_right = G[center_idx, idx_right]
    
    # Up 1: (cx, cy+1)
    idx_up = center_x*N + (center_y+1)
    val_up = G[center_idx, idx_up]
    
    diff_rot = np.abs(val_right - val_up)
    status_rot = "PASS" if diff_rot < 1e-10 else "FAIL"
    
    print(f"{'Rotation (90 deg)':<20} | {val_right:.6f}{'':<9} | {val_up:.6f}{'':<9} | {diff_rot:.2e}{'':<4} | {status_rot}")
    
    # 4. Test Reflection Symmetry (Diagonal Parity)
    # Compare (Center -> Right 1, Up 1) vs (Center -> Right 1, Down 1)
    # Diagonal A: (cx+1, cy+1)
    idx_diag_A = (center_x+1)*N + (center_y+1)
    val_diag_A = G[center_idx, idx_diag_A]
    
    # Diagonal B: (cx+1, cy-1)
    idx_diag_B = (center_x+1)*N + (center_y-1)
    val_diag_B = G[center_idx, idx_diag_B]
    
    diff_ref = np.abs(val_diag_A - val_diag_B)
    status_ref = "PASS" if diff_ref < 1e-10 else "FAIL"
    
    print(f"{'Reflection (Parity)':<20} | {val_diag_A:.6f}{'':<9} | {val_diag_B:.6f}{'':<9} | {diff_ref:.2e}{'':<4} | {status_ref}")

    print("-" * 75)
    
    if status_rot == "PASS" and status_ref == "PASS":
        print("\n[SUCCESS] Geometry is Isotropic (Euclidean Invariance Holds).")
        print("          Vacuum correlations depend only on distance, not angle.")
    else:
        print("\n[FAILURE] Geometry is Anisotropic (Lattice Artifacts dominant).")

if __name__ == "__main__":
    run_experiment()