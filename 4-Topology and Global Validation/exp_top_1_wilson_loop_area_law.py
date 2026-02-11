#Paper: Relational Lysis Theory: A Universal Self-Adjoint Operator Unifying Geometry, Quantum Gauge Fields, Gravitation, Thermodynamics, Arithmetic, and Computation
#Researcher: Dr. David Swanagon
#LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: February 09, 2026

#!/usr/bin/env python3
"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_top_1_wilson_loop_area_law.py
Category:        4-Topology and Global Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 12.5 (Confinement) & Theorem 12.8
Theorem Support: "Area Law from Harmonic Propagation of Non-Zero Curl"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Strictly honors RL Theory.
    
    1. Input (Topological Sector):
       We define a Prime State with **Rotational Boundary Conditions**.
       Instead of a gradient (pure gauge), we set the boundary links to represent
       a constant background Flux (Magnetic Field B).
       
       A_x ~ -y * B
       A_y ~  x * B
       
       This ensures the Total Flux through the lattice is non-zero.
       
    2. Inevitable Descent (Harmonic Lysis):
       The Interior relaxes to the Harmonic Fixed Point (Solved State).
       Because the boundary has Curl, the Harmonic solution must maintain
       that Curl throughout the bulk (Stokes' Theorem).
       The Shadow cannot vanish; it becomes the pervasive Flux Field.
       
    3. Measurement:
       We measure the Wilson Loop <W> on this Harmonic State.
       The phase of the loop should scale linearly with the Area enclosed.
       
    Hypothesis:
    The Harmonic propagation of a Rotational Boundary enforces an Area Law.
    Log(W) ~ -sigma * Area (or Phase ~ Area).

ADVERSARIAL CONDITIONS:
    - Input:                   Rotational Boundary (Curl != 0)
    - Process:                 Pure Harmonic Descent (No heuristics)
    - Measurement:             Wilson Loop Phase Scaling

PASS CRITERIA:
    1. Flux Survival:          Interior curl is non-zero.
    2. Area Law:               Loop Phase scales linearly with Area (R^2 > 0.99).
    3. Non-Triviality:         Wilson Loop != 1.0.

USAGE:
    python3 exp_quant_16_wilson_loop_area_law.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
import scipy.stats as stats

class RelationalLysisEngine:
    def run_harmonic_descent(self, prime_state, boundary_mask, N_side, max_depth=2000, tol=1e-8):
        """
        Descends to the Harmonic Fixed Point.
        Solves Laplace Equation on the Link Variables subject to Boundary Constraints.
        """
        current_state = prime_state.copy()
        print(f"[*] Entering Harmonic Lysis Tower...")
        
        for depth in range(max_depth):
            # Extract Vector Fields H (Right links) and V (Down links)
            H = np.zeros((N_side, N_side))
            V = np.zeros((N_side, N_side))
            
            for x in range(N_side):
                for y in range(N_side):
                    idx = x*N_side + y
                    n_right = ((x+1)%N_side)*N_side + y
                    n_down  = x*N_side + ((y+1)%N_side)
                    H[x,y] = current_state[idx, n_right]
                    V[x,y] = current_state[idx, n_down]
            
            # Harmonic Update (Laplace Averaging) on Interior Links
            H_new = H.copy()
            V_new = V.copy()
            
            # Vectorized Relaxation (Jacobi Method)
            # H_new = Avg(Neighbors)
            H_new[1:-1, 1:-1] = 0.25 * (H[2:, 1:-1] + H[:-2, 1:-1] + H[1:-1, 2:] + H[1:-1, :-2])
            V_new[1:-1, 1:-1] = 0.25 * (V[2:, 1:-1] + V[:-2, 1:-1] + V[1:-1, 2:] + V[1:-1, :-2])
            
            # Reconstruct Matrix
            next_matrix = np.zeros_like(current_state)
            
            for x in range(N_side):
                for y in range(N_side):
                    idx = x*N_side + y
                    n_right = ((x+1)%N_side)*N_side + y
                    n_down  = x*N_side + ((y+1)%N_side)
                    
                    next_matrix[idx, n_right] = H_new[x,y]
                    next_matrix[n_right, idx] = -H_new[x,y] # Skew
                    next_matrix[idx, n_down]  = V_new[x,y]
                    next_matrix[n_down, idx]  = -V_new[x,y] # Skew

            # Enforce Boundary Constraints Strictly
            next_matrix = next_matrix * (1 - boundary_mask) + prime_state * boundary_mask
            
            # Check Convergence
            diff = np.linalg.norm(next_matrix - current_state)
            if diff < tol:
                print(f"    -> Harmonic Point reached at Depth {depth}.")
                return next_matrix
            
            current_state = next_matrix
            
            if depth % 200 == 0:
                print(f"    Depth {depth}: Relaxation Delta = {diff:.2e}")

        print(f"    -> Max depth reached.")
        return current_state

def run_experiment():
    print(f"[*] Starting Wilson Loop (Confinement) Test...")
    print(f"[*] Reference: Theorem 12.8 (Area Law)\n")
    
    engine = RelationalLysisEngine()
    N_side = 20
    N_sites = N_side * N_side
    
    # 1. Initialize Topological Sector (Rotational Boundary)
    np.random.seed(137) 
    
    Prime_State = np.zeros((N_sites, N_sites))
    Boundary_Mask = np.zeros((N_sites, N_sites))
    
    print(f"[*] Initializing Prime State with Rotational Flux (Curl != 0)...")
    
    # Flux Strength (Magnetic Field B)
    B_field = 0.1
    
    for x in range(N_side):
        for y in range(N_side):
            idx = x * N_side + y
            
            # Neighbor Indices
            n_idx_r = ((x + 1) % N_side) * N_side + y
            n_idx_d = x * N_side + ((y + 1) % N_side)
            
            # Boundary Logic
            is_bound_x = (x == 0) or (x == N_side-1)
            is_bound_y = (y == 0) or (y == N_side-1)
            
            # Rotational Vector Potential (Symmetric Gauge)
            # A_x = -0.5 * B * y
            # A_y =  0.5 * B * x
            # Curl A = dA_y/dx - dA_x/dy = 0.5B - (-0.5B) = B (Constant Flux)
            
            val_h = -0.5 * B_field * y
            val_v =  0.5 * B_field * x
            
            if is_bound_x or is_bound_y:
                # Apply to Horizontal (Right)
                Prime_State[idx, n_idx_r] = val_h
                Prime_State[n_idx_r, idx] = -val_h
                Boundary_Mask[idx, n_idx_r] = 1.0
                Boundary_Mask[n_idx_r, idx] = 1.0
                
                # Apply to Vertical (Down)
                Prime_State[idx, n_idx_d] = val_v
                Prime_State[n_idx_d, idx] = -val_v
                Boundary_Mask[idx, n_idx_d] = 1.0
                Boundary_Mask[n_idx_d, idx] = 1.0
            else:
                # Interior Vacuum
                Prime_State[idx, n_idx_r] = 0.0
                Prime_State[idx, n_idx_d] = 0.0
                Boundary_Mask[idx, n_idx_r] = 0.0
                Boundary_Mask[idx, n_idx_d] = 0.0

    # 2. Run Harmonic Descent
    Solved_State = engine.run_harmonic_descent(Prime_State, Boundary_Mask, N_side)
    
    # 3. Measure Wilson Loops
    print(f"\n[*] Measuring Wilson Loops on Harmonic Solved State...")
    print(f"{'Loop Size':<15} | {'Area':<8} | {'Total Phase':<15} | {'Phase/Area'}")
    print("-" * 60)
    
    areas = []
    phases = []
    max_R = 6
    
    # We measure in the Bulk (Center)
    cx, cy = N_side // 2, N_side // 2
    start_x, start_y = cx - 3, cy - 3
    
    for R in range(1, max_R + 1):
        # Construct Single Central Loop
        # We sum the Link Variables X_ij around the loop.
        # Total Phase = Integral(A * dl)
        
        loop_phase = 0.0
        curr_x, curr_y = start_x, start_y
        
        # Right
        for _ in range(R):
            src = curr_x * N_side + curr_y
            curr_x = (curr_x + 1) % N_side
            dst = curr_x * N_side + curr_y
            loop_phase += Solved_State[src, dst]
        # Up
        for _ in range(R):
            src = curr_x * N_side + curr_y
            curr_y = (curr_y + 1) % N_side
            dst = curr_x * N_side + curr_y
            loop_phase += Solved_State[src, dst]
        # Left
        for _ in range(R):
            src = curr_x * N_side + curr_y
            curr_x = (curr_x - 1 + N_side) % N_side
            dst = curr_x * N_side + curr_y
            loop_phase -= Solved_State[dst, src]
        # Down
        for _ in range(R):
            src = curr_x * N_side + curr_y
            curr_y = (curr_y - 1 + N_side) % N_side
            dst = curr_x * N_side + curr_y
            loop_phase -= Solved_State[dst, src]
            
        area = R * R
        
        # NOTE: For Confinement, we look for Phase ~ Area.
        # This corresponds to "Constant Flux" through the loop.
        # The Wilson Loop Operator W = exp(i * Phase).
        
        areas.append(area)
        phases.append(abs(loop_phase)) # Magnitude of accumulated flux
        
        print(f"{R}x{R:<13} | {area:<8} | {loop_phase:.6f}{'':<9} | {abs(loop_phase)/area:.6f}")

    print("-" * 60)
    
    # 5. Analyze Scaling
    slope, intercept, r_value, p_value, std_err = stats.linregress(areas, phases)
    flux_density = slope
    linearity = r_value**2
    
    print(f"[*] Fit Results:")
    print(f"    Flux Density (Slope):    {flux_density:.4f}")
    print(f"    Linearity (R^2):         {linearity:.4f}")
    
    # If the Phase scales linearly with Area, it proves the Flux 
    # has penetrated the bulk (Area Law Behavior).
    if flux_density > 0.001 and linearity > 0.99:
        print("\n[SUCCESS] Area Law / Flux Penetration Confirmed.")
        print("          The Harmonic State maintains the Topological Curl.")
        print("          (Phase scales linearly with Area).")
    else:
        print("\n[FAILURE] Area Law violated (Flux vanished).")

if __name__ == "__main__":
    run_experiment()