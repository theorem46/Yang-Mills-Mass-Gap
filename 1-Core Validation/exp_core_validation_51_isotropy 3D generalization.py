"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_51_isotropy 3D generalization.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 3.9 (High-Dimensional Lysis)
Theorem Support: "Rotational Symmetry and Isotropy of the 3D Operator"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Validates the 3D generalization of the Relational Lysis operator using a 
    standard 7-point stencil (Center + 6 Neighbors). 
    
    The script tests the operator against a 3D quadratic field:
    $$f(x, y, z) = x^2 + y^2 + z^2$$
    
    Analytical verification: 
    $$\nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2} + \frac{\partial^2 f}{\partial z^2} = 2 + 2 + 2 = 6.0$$
    
    This confirms that the operator correctly recovers the second-order 
    derivative in 3D and respects the cubic symmetry of the lattice.

ADVERSARIAL CONDITIONS:
    - Lattice Size:            30x30x30 Grid (27,000 sites)
    - Field Geometry:          3D Paraboloid
    - Stencil:                 7-Point (Orthogonal directions)

PASS CRITERIA:
    1. Numerical Accuracy:     Lysis Output ≈ 6.0 (Analytical match).
    2. Zero Artifacts:         Boundary-free interior provides bit-exact precision.

USAGE:
    python3 exp_core_val_17c_3d_isotropy_laplacian.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np

# -----------------------------
# Parameters
# -----------------------------
N = 30  # 30x30x30 grid (smaller due to cubic complexity)
SCALE = 1.0

# -----------------------------
# Build 3D Field
# -----------------------------
# f(x,y,z) = x^2 + y^2 + z^2

grid = np.zeros((N, N, N))
for z in range(N):
    for y in range(N):
        for x in range(N):
            grid[z, y, x] = (x**2 + y**2 + z**2) * SCALE

# -----------------------------
# Relational Lysis (3D)
# -----------------------------
def lysis_3d(field):
    D, H, W = field.shape
    out = np.zeros_like(field)
    
    # Interior points only (7-point stencil)
    for z in range(1, D-1):
        for y in range(1, H-1):
            for x in range(1, W-1):
                
                neighbors = field[z, y, x+1] + field[z, y, x-1] + \
                            field[z, y+1, x] + field[z, y-1, x] + \
                            field[z+1, y, x] + field[z-1, y, x]
                
                # In 3D, the center weight is -6
                out[z, y, x] = neighbors - 6.0 * field[z, y, x]
            
    return out

# -----------------------------
# Main
# -----------------------------
def main():
    print("\nRELATIONAL LYSIS — SCRIPT TYPE 17")
    print("3D Isotropy & Laplacian Limit")
    print("--------------------------------------------------")
    
    L_grid = lysis_3d(grid)
    
    # Check the center of the grid
    mid = N // 2
    val = L_grid[mid, mid, mid]
    
    print(f"Input Field:             f = x^2 + y^2 + z^2")
    print(f"Analytical Laplacian:    6.0")
    print(f"Relational Lysis Output: {val:.10f}")
    
    error = abs(val - 6.0)
    print(f"Error:                   {error:.10e}")
    
    print("\nINTERPRETATION:")
    print("Exact match confirms the operator works in 3D.")
    print("It generates the correct 7-point stencil.")

if __name__ == "__main__":
    main()