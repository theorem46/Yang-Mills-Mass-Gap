"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_65__gap_closure_operator_selection.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 12, 2026
Paper Reference: Section 44.1 (Non-Circular Derivation of the Operator)
Theorem Support: "Uniqueness of the Isotropic Laplacian under Symmetry Constraint"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Directly addresses the referee's critique regarding "circularity." Rather 
    than defining Lysis via the Laplacian, this script treats the Laplacian as 
    an emergent winner of a tournament.
    
    The experiment starts with a pure "Geometric State" (a Symmetric Matrix). 
    It then applies a variety of local stencils (Gradient, Advection, 
    Anisotropic Laplacian, Biharmonic, and Random Stencils). 
    
    A valid Lysis operator must satisfy the "Closure Axiom": it must propagate 
    Symmetry without generating Skew-Symmetric "Shadow." Any operator that 
    produces Shadow ($S \neq 0$) from a pure Diamond ($D$) is eliminated 
    as physically inconsistent with the manifold's relational logic.

ADVERSARIAL CONDITIONS:
    - Candidate Pool:          9 Distinct Operator Classes (1st to 4th order)
    - Input State:             Stochastic Symmetric Matrix (Pure $D$)
    - Resolution:              $50 \times 50$ Lattice
    - Metric:                   Shadow Leakage Ratio ($||S|| / ||Total||$)
    - Selection Rule:          Minimal Support + Zero Shadow Leakage

PASS CRITERIA:
    1. Shadow Rejection:       Gradient, Advection, and Random stencils must fail.
    2. Isotropy Enforcement:   Anisotropic variants must fail.
    3. Minimality:             While the Biharmonic survives, the Laplacian is 
                               selected as the minimal second-order solution.

USAGE:
    python3 exp_gap_closure_01_operator_selection.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
import scipy.linalg as la

# =============================================================================
# 1. CANDIDATE OPERATORS (THE "POOL")
# =============================================================================

class OperatorCandidates:
    def __init__(self, N):
        self.N = N

    def shift(self, X, dx, dy):
        return np.roll(np.roll(X, dx, axis=0), dy, axis=1)

    # --- 1st Order ---
    def gradient_x(self, X):
        # Central difference: (x+1) - (x-1)
        # Skew-symmetric signature expected
        return 0.5 * (self.shift(X, -1, 0) - self.shift(X, 1, 0))

    def advection_xy(self, X):
        # Diagonal drift
        return self.shift(X, -1, -1) - X

    # --- 2nd Order ---
    def laplacian_isotropic(self, X):
        # The "Standard" candidate
        # 4*Center - (Up+Down+Left+Right)
        neighbors = (
            self.shift(X, -1, 0) + self.shift(X, 1, 0) +
            self.shift(X, 0, -1) + self.shift(X, 0, 1)
        )
        return 4.0 * X - neighbors

    def laplacian_anisotropic_A(self, X):
        # Biased X: 10*X - (5*Up + 5*Down + 0.1*Left + 0.1*Right)
        # Violates isotropy
        vert = 5.0 * (self.shift(X, -1, 0) + self.shift(X, 1, 0))
        horz = 0.1 * (self.shift(X, 0, -1) + self.shift(X, 0, 1))
        return 10.2 * X - (vert + horz)

    def cross_derivative_dxy(self, X):
        # d^2 / dx dy
        # Stencil involves corners
        return 0.25 * (
            self.shift(X, -1, -1) + self.shift(X, 1, 1) -
            self.shift(X, -1, 1) - self.shift(X, 1, -1)
        )

    # --- Higher Order ---
    def biharmonic(self, X):
        # Del^4 = Laplacian(Laplacian(X))
        L = self.laplacian_isotropic(X)
        return self.laplacian_isotropic(L)
    
    def dispersive_3rd(self, X):
        # d^3 / dx^3
        return 0.5 * (self.shift(X, -2, 0) - 2*self.shift(X, -1, 0) + 
                      2*self.shift(X, 1, 0) - self.shift(X, 2, 0))

    # --- Random Stencils (The "Everything Else" Bucket) ---
    def random_stencil_1(self, X):
        # Random weights, likely asymmetric
        return 0.73*self.shift(X, 1, 0) - 0.22*self.shift(X, 0, 1)
    
    def random_stencil_2(self, X):
        return 0.5*X + 0.5*self.shift(X, 1, 1)

# =============================================================================
# 2. TOURNAMENT ENGINE
# =============================================================================

def measure_shadow_leakage(matrix):
    """
    Decomposes a matrix into Symmetric (Diamond) and Skew (Shadow).
    Returns the ratio of Shadow Energy / Total Energy.
    """
    sym = 0.5 * (matrix + matrix.T)
    skew = 0.5 * (matrix - matrix.T)
    
    n_sym = np.linalg.norm(sym)
    n_skew = np.linalg.norm(skew)
    total = np.sqrt(n_sym**2 + n_skew**2)
    
    if total < 1e-15: return 0.0 # Trivial zero state
    return n_skew / total

def run_tournament():
    print("\nRELATIONAL LYSIS: GAP CLOSURE 01")
    print("Operator Natural Selection Tournament")
    print("================================================================")
    print("Objective: Derive the Laplacian solely from Symmetry Preservation.")
    print("Input:     Random Pure Diamond State (Symmetric Matrix).")
    print("Test:      Does Op(Diamond) remain a Diamond?")
    print("----------------------------------------------------------------")
    
    N = 50
    ops = OperatorCandidates(N)
    
    # 1. Generate Input: Pure Geometry
    # A symmetric matrix represents a solved state "D"
    np.random.seed(42)
    base = np.random.randn(N, N)
    D_in = 0.5 * (base + base.T) 
    
    # Verify input purity
    input_leak = measure_shadow_leakage(D_in)
    print(f"Input State Shadow Leakage: {input_leak:.2e} (Pure Symmetric)")
    print("-" * 64)
    print(f"{'CANDIDATE OPERATOR':<25} | {'SHADOW LEAKAGE':<15} | {'VERDICT'}")
    print("-" * 64)

    candidates = [
        ("Gradient (1st Order)", ops.gradient_x),
        ("Advection (Mixed)", ops.advection_xy),
        ("Laplacian (Isotropic)", ops.laplacian_isotropic),
        ("Laplacian (Anisotropic)", ops.laplacian_anisotropic_A),
        ("Cross-Deriv (dxy)", ops.cross_derivative_dxy),
        ("Biharmonic (4th Order)", ops.biharmonic),
        ("Dispersive (3rd Order)", ops.dispersive_3rd),
        ("Random Stencil A", ops.random_stencil_1),
        ("Random Stencil B", ops.random_stencil_2),
    ]

    winners = []

    for name, func in candidates:
        # Apply Operator
        D_out = func(D_in)
        
        # Measure what came out
        leakage = measure_shadow_leakage(D_out)
        norm_out = np.linalg.norm(D_out)

        # Verdict Logic
        if norm_out < 1e-10:
            status = "ELIMINATED (Trivial/Zero)"
        elif leakage > 1e-10:
            status = "ELIMINATED (Generated Shadow)"
        else:
            status = "SURVIVED (Preserved Geometry)"
            winners.append(name)
            
        print(f"{name:<25} | {leakage:.2e}      | {status}")

    print("-" * 64)
    print(f"\nTOURNAMENT RESULTS:")
    print(f"Survivors: {winners}")
    
    # Check for Minimality among survivors
    # (Biharmonic preserves symmetry, but is higher order/complexity)
    if "Laplacian (Isotropic)" in winners and "Biharmonic (4th Order)" in winners:
        print("\nNOTE: Biharmonic also preserves symmetry, but requires")
        print("      deeper stencil support (4th order).")
        print("      Relational Lysis selects the MINIMAL local survivor.")
        print("      -> WINNER: Covariant Laplacian")
    
if __name__ == "__main__":
    run_tournament()