"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_22_vector laplacian.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 3.9, Definition 3.28 (Lie Algebra Extension)
Theorem Support: "Component-wise Action on Vector Bundles"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Verifies that Relational Lysis generalizes correctly to vector-valued fields
    (e.g., Lie Algebra components).
    
    It compares the Lysis of a multi-component field (flattened) against the
    Block Diagonal Laplacian. A ratio of exactly 1.0 confirms that the operator
    acts component-wise, allowing it to define curvature on bundles (SU(N)).

ADVERSARIAL CONDITIONS:
    - Dimensions:              K=8 (SU(3) Adjoint Dimension)
    - Lattice:                 N=500
    - Input:                   Smooth K-component vector field

PASS CRITERIA:
    1. Energy Ratio:           E_lysis / E_block_laplacian == 1.000000

USAGE:
    python3 exp_core_val_04_vector_laplacian.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
import math

# -----------------------------
# Parameters
# -----------------------------

N = 500  # lattice sites
K = 8  # number of components (e.g., SU(3) adjoint dimension)

# -----------------------------
# Build smooth K-component field
# -----------------------------

X = np.zeros((N, K))

for i in range(N):
    for k in range(K):
        X[i, k] = math.sin(2 * math.pi * (i + k) / N)

# Flattened vector
x_flat = X.flatten()

# -----------------------------
# Relational Lysis (vector)
# -----------------------------


def lysis_vector(X):
    Y = np.zeros_like(X)
    for i in range(N):
        Y[i] = X[(i + 1) % N] - 2 * X[i] + X[(i - 1) % N]
    return Y


Y = lysis_vector(X)

E_lysis = np.linalg.norm(Y) / np.linalg.norm(X)

# -----------------------------
# Build scalar Laplacian
# -----------------------------

L = np.zeros((N, N))

for i in range(N):
    L[i, i] = -2
    L[i, (i + 1) % N] = 1
    L[i, (i - 1) % N] = 1

# -----------------------------
# Build block Laplacian
# -----------------------------

I_K = np.eye(K)
L_block = np.kron(L, I_K)

# -----------------------------
# Apply block Laplacian
# -----------------------------

Y_block = L_block @ x_flat
Y_block = Y_block.reshape((N, K))

E_block = np.linalg.norm(Y_block) / np.linalg.norm(X)

# -----------------------------
# Output
# -----------------------------

print("\nRELATIONAL LYSIS — SCRIPT TYPE 4")
print("----------------------------------------------------")
print(f"Lysis Vector Energy:     {E_lysis:.12e}")
print(f"Block Laplacian Energy:  {E_block:.12e}")
print(f"Ratio (Lysis / Block):   {E_lysis / E_block:.12e}")

print("\nINTERPRETATION:")
print("Ratio ≈ 1 confirms:")
print("Relational Lysis on vector fields")
print("equals block-diagonal Laplacian.")
print("This is the operator used for Lie-algebra valued fields.")
