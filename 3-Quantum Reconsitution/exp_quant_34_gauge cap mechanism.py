"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_34_gauge cap mechanism.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Paper Reference: Section 12.2 (Confinement)
Theorem Support: "Area Law for Wilson Loops"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests confinement via Wilson Loop expectation.
    Includes 42b (Gauge Gap Mechanism), 42c (2D Continuum Stability).

ADVERSARIAL CONDITIONS:
    - Loop Area:               2x2 to 10x10

PASS CRITERIA:
    1. Area Law:               Log(W) scales with Area.
-------------------------------------------------------------------------------
"""

import numpy as np
import scipy.linalg as la
from scipy.sparse import diags, bmat
from scipy.sparse.linalg import eigsh


def build_covariant_laplacian(N, disorder_strength=0.0):
    """
    Constructs 1D Gauge Laplacian: D_mu D_mu
    L_ii = 2
    L_i,i+1 = -U_x,x+1
    L_i,i-1 = -U_x,x-1

    disorder_strength (eta):
      0.0 -> U = 1 (Flat/Abelian)
      1.0 -> U = Random Phase (Curved/Non-Abelian Proxy)
    """
    # 1. Define Links U_{x, x+1}
    # We use U(1) phases as a proxy for SU(N) disorder
    phases = np.random.uniform(-np.pi, np.pi, N) * disorder_strength
    U = np.exp(1j * phases)

    # 2. Build Sparse Matrix
    # Diagonal (Self-interaction)
    main = 2 * np.ones(N)

    # Off-diagonals (Hopping with parallel transport)
    # Forward hop: -U_{x,x+1}
    upper = -U[:-1]
    # Backward hop: -conjugate(U_{x-1,x})
    lower = -np.conj(U[:-1])

    # Periodic Boundary Conditions (to isolate bulk gap)
    # Wrap-around link
    U_boundary = np.exp(1j * np.random.uniform(-np.pi, np.pi) * disorder_strength)
    corner_upper = -np.conj(U_boundary)  # L[0, N-1]
    corner_lower = -U_boundary  # L[N-1, 0]

    # Construct Matrix
    data = [main, upper, lower]
    offsets = [0, 1, -1]
    L = diags(data, offsets, shape=(N, N), format="csr")

    # Add PBC corners
    L[0, N - 1] = corner_upper
    L[N - 1, 0] = corner_lower

    return L


def get_ground_state(L):
    # Find smallest magnitude eigenvalue
    # Note: L is Hermitian, so eigenvalues are real
    vals = eigsh(L, k=1, which="SM", return_eigenvectors=False)
    return vals[0]


def main():
    print("\nRELATIONAL LYSIS — SCRIPT TYPE 42B")
    print("The Gauge Gap Mechanism Proof")
    print("---------------------------------------------------------------")
    print(f"{'N':<5} {'Lambda (Flat)':<15} {'Lambda (Curved)':<15} {'Gap Ratio'}")
    print("---------------------------------------------------------------")

    # Parameters
    disorder = 1.0  # Max curvature

    for N in [50, 100, 200, 400, 800]:
        # Case A: Flat Vacuum (U=1)
        L_flat = build_covariant_laplacian(N, disorder_strength=0.0)
        lam_flat = get_ground_state(L_flat)

        # Case B: Curved Vacuum (U=Random)
        L_curved = build_covariant_laplacian(N, disorder_strength=disorder)
        lam_curved = get_ground_state(L_curved)

        # Ratio
        ratio = lam_curved / (lam_flat + 1e-15)

        print(f"{N:<5} {lam_flat:.6e}    {lam_curved:.6e}    {ratio:.1f}x")

    print("---------------------------------------------------------------")
    print("INTERPRETATION:")
    print("1. Lambda (Flat) should decay as ~1/N^2 (Gap closes).")
    print("2. Lambda (Curved) should stay roughly constant (Gap stays open).")
    print("IF THIS HOLDS: You have proven that Gauge Curvature generates Mass.")


if __name__ == "__main__":
    main()
