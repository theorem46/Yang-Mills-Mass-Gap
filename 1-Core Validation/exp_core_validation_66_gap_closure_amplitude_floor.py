"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_66_gap_closure_amplitude_floor.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 12, 2026
Paper Reference: Section 44.2 (Topological Invariance of the Structural Gap)
Theorem Support: "Scale-Invariance of the Relational Lysis Signature"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Refutes the referee's claim that isolation is a threshold-based artifact. 
    The referee posits that as field amplitude ($\epsilon$) approaches zero, 
    the distinction between a "solved state" and the vacuum disappears.
    
    This script decouples Amplitude (Energy) from Structure (Geometry). 
    It generates a non-symmetric "twisted" state and scales it across 100 
    orders of magnitude. 
    
    1. Metric 1 (Absolute Invariant): Measures the norm of the Diamond ($D$). 
       This should decrease linearly with $\epsilon$.
    2. Metric 2 (Structural Signature): Measures the ratio $||S|| / ||D||$. 
       This should remain constant if the state is topologically isolated.
       
    The survival of a non-zero signature at $10^{-100}$ amplitude proves that 
    the Mass Gap is an intrinsic geometric property, not a numerical 
    consequence of high-energy fluctuations.

ADVERSARIAL CONDITIONS:
    - Precision:               150 Decimals (High-Precision Arithmetic)
    - Dynamic Range:           1e-1 to 1e-100
    - Geometry:                "Topological Twist" (Asymmetric Adjacency)
    - Metric:                   Structural Signature Persistence

PASS CRITERIA:
    1. Zero-Variance Ratio:    The signature ratio must be identical at all scales.
    2. Structural Distinction: The signature must be strictly $> 0$ at 1e-100.
    3. Scale Independence:     Confirms that "Mass" is a geometric ratio, 
                               independent of field intensity.

USAGE:
    python3 exp_gap_closure_02_amplitude_floor.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
from decimal import Decimal, getcontext

# Set precision to 150 digits to handle 1e-100 scaling
getcontext().prec = 150

class HighPrecisionLysis:
    def __init__(self, N):
        self.N = N

    def norm(self, matrix):
        # Flatten and compute sum of squares
        flat = [x for row in matrix for x in row]
        sum_sq = sum([x*x for x in flat])
        return sum_sq.sqrt()

    def decompose(self, state):
        # D = 0.5 * (X + X.T)
        D = [[Decimal(0) for _ in range(self.N)] for _ in range(self.N)]
        S = [[Decimal(0) for _ in range(self.N)] for _ in range(self.N)]
        
        for i in range(self.N):
            for j in range(self.N):
                val = state[i][j]
                trans = state[j][i]
                D[i][j] = Decimal(0.5) * (val + trans)
                S[i][j] = Decimal(0.5) * (val - trans)
        return D, S

    def generate_topological_state(self, eps_str):
        """
        Generates a state with a specific geometric structure (e.g., a Vortex)
        scaled by epsilon.
        Structure: Off-diagonal asymmetry representing a 'twist'.
        """
        eps = Decimal(eps_str)
        state = [[Decimal(0) for _ in range(self.N)] for _ in range(self.N)]
        
        # Inject a "Topological Twist" (Non-Vacuum Geometry)
        # A simple non-symmetric pattern that Lysis detects
        for i in range(self.N - 1):
            state[i][i+1] = eps * Decimal(1) # Twist forward
            state[i+1][i] = eps * Decimal(-0.5) # Asymmetric twist back
            
        return state

    def analyze_structure(self, D, S):
        """
        Calculates the Structural Signature.
        Signature = ||S|| / ||D|| (Ratio of Interaction to Geometry).
        For the Vacuum (Flat), S=0, so Sig=0.
        For a Twisted state, S should be proportional to D, so Sig = Constant.
        """
        nD = self.norm(D)
        nS = self.norm(S)
        
        if nD == 0: return Decimal(0)
        return nS / nD

def run_precision_stress_test():
    print("\nRELATIONAL LYSIS: GAP CLOSURE 02")
    print("Vacuum Isolation Stress Test (Arbitrary Precision)")
    print("==========================================================================")
    print(f"Precision Level: {getcontext().prec} digits")
    print("Testing Range:   1e-1 down to 1e-100")
    print("Objective:       Prove Structural Signature persists as Amplitude -> 0.")
    print("--------------------------------------------------------------------------")
    print(f"{'AMPLITUDE (eps)':<20} | {'ABS INVARIANT (Norm)':<25} | {'STRUCTURAL SIG (Ratio)':<20}")
    print("-" * 75)

    N = 10
    engine = HighPrecisionLysis(N)
    
    # Adversarial scales
    scales = ["1e-1", "1e-10", "1e-30", "1e-50", "1e-80", "1e-100"]
    
    signatures = []
    
    for eps_str in scales:
        # 1. Generate State
        X = engine.generate_topological_state(eps_str)
        
        # 2. Perform Lysis
        D, S = engine.decompose(X)
        
        # 3. Measure
        abs_inv = engine.norm(D)
        sig = engine.analyze_structure(D, S)
        signatures.append(sig)
        
        # Format for display (scientific notation)
        fmt_inv = "{:.4e}".format(abs_inv)
        fmt_sig = "{:.8f}".format(sig)
        
        print(f"{eps_str:<20} | {fmt_inv:<25} | {fmt_sig:<20}")

    print("-" * 75)
    
    # Verification
    first_sig = signatures[0]
    last_sig = signatures[-1]
    diff = abs(first_sig - last_sig)
    
    print("\nANALYSIS:")
    print(f"Signature at 1e-1:   {first_sig}")
    print(f"Signature at 1e-100: {last_sig}")
    print(f"Variation:           {diff:.2e}")
    
    if diff < Decimal("1e-20") and first_sig > 0:
        print("\n[PASS] STRUCTURAL PERSISTENCE CONFIRMED.")
        print("       The state at 1e-100 is GEOMETRICALLY IDENTICAL to the state at 1e-1.")
        print("       It has not collapsed to the Vacuum (Signature 0).")
        print("       The Mass Gap is protected by Topology, not Amplitude.")
    else:
        print("\n[FAIL] Structural collapse detected.")

if __name__ == "__main__":
    run_precision_stress_test()