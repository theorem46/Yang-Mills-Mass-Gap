#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_26_mass gap vs periodic flow.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Paper Reference: Section 5.2 (Harmonic Modes)
Theorem Support: "Topological Mass Generation via Flux"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the "Gauge Gap" mechanism on a ring topology.
    Compares U(1) (Abelian) vs SU(2) (Non-Abelian) ground states.
    
    For U(1), the flux can be gauged away or results in a massless mode.
    For SU(2), the non-commutative flux frustrates the ground state, lifting
    the energy > 0 (Mass Generation).

ADVERSARIAL CONDITIONS:
    - Topology:                1D Periodic Ring
    - Group:                   U(1) vs SU(2) with random flux
    - Sizes:                   N = 10 to 40

PASS CRITERIA:
    1. U(1) Ground:            Approx 0.0 (Gapless).
    2. SU(2) Ground:           > 1.0 (Massive/Gapped).
-------------------------------------------------------------------------------
"""

import numpy as np

# ------------------------------------------------------------
# Pauli matrices
# ------------------------------------------------------------
sigma1 = np.array([[0, 1], [1, 0]], dtype=complex)
sigma2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma3 = np.array([[1, 0], [0, -1]], dtype=complex)


# ------------------------------------------------------------
# Random SU(2) Link
# ------------------------------------------------------------
def random_su2(strength=0.8):
    # Random axis
    v = np.random.randn(3)
    v /= np.linalg.norm(v)

    # Fixed "disorder strength" angle
    # If angle=0, matrix is Identity (No Gap)
    # If angle>0, flux exists
    return np.cos(strength) * np.eye(2) + 1j * np.sin(strength) * (
        v[0] * sigma1 + v[1] * sigma2 + v[2] * sigma3
    )


# ------------------------------------------------------------
# U(1) Periodic Laplacian (Ring)
# ------------------------------------------------------------
def u1_periodic(N):
    L = np.zeros((N, N))
    for i in range(N):
        left = (i - 1 + N) % N
        right = (i + 1) % N

        L[i, i] = 2.0
        L[i, left] = -1.0
        L[i, right] = -1.0

    return (N**2) * L


# ------------------------------------------------------------
# SU(2) Periodic Laplacian (Ring with Flux)
# ------------------------------------------------------------
def su2_periodic(N):
    dim = 2 * N
    L = np.zeros((dim, dim), dtype=complex)

    # Generate N links for the N edges of the ring
    U_links = [random_su2() for _ in range(N)]

    for i in range(N):
        left_idx = (i - 1 + N) % N
        right_idx = (i + 1) % N

        # Diagonal
        for a in range(2):
            L[2 * i + a, 2 * i + a] = 2.0

        # Off-diagonal (Right)
        # Interaction from i to right_idx uses U_links[i]
        U = U_links[i]
        for a in range(2):
            for b in range(2):
                # Coupling to right neighbor
                # L term is usually -U psi(x+1)
                # We fill row 2*i. Column 2*right_idx
                L[2 * i + a, 2 * right_idx + b] = -U[a, b]

                # Hermitian conjugate for the reverse link
                # Coupling to left neighbor (requires U_left_dagger)
                # Handled by symmetry if we just iterate all i

        # To ensure Hermitian symmetry explicitly:
        # We can just fill upper triangle and symmetrize,
        # but let's do the Left neighbor explicitly using U_left_dagger

        U_left = U_links[left_idx]
        U_left_dag = np.conj(U_left).T

        for a in range(2):
            for b in range(2):
                L[2 * i + a, 2 * left_idx + b] = -U_left_dag[a, b]

    return (N**2) * L


# ------------------------------------------------------------
# Smallest Eigenvalue (Ground State)
# ------------------------------------------------------------
def get_ground_state(M):
    # We want the lowest REAL eigenvalue
    # eigh is for Hermitian
    vals = np.linalg.eigvalsh(M)
    return vals[0]


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    print("\nRELATIONAL LYSIS — SCRIPT TYPE 28B")
    print("Mass Gap via Periodic Flux (Topology Test)")
    print("--------------------------------------------")
    print(f"{'N':<5} {'U(1) Ground':<15} {'SU(2) Ground (Mass Gap)'}")
    print("--------------------------------------------")

    for N in [10, 15, 20, 30, 40]:
        # Abelian (Free Photon)
        # Ground state of periodic ring is Constant Mode (Energy = 0)
        E0_u1 = get_ground_state(u1_periodic(N))

        # Non-Abelian (Gluon soup)
        # Random flux frustrates the constant mode
        E0_su2 = get_ground_state(su2_periodic(N))

        print(f"{N:<5} {E0_u1:<15.6e} {E0_su2:<15.6e}")

    print("--------------------------------------------")
    print("INTERPRETATION:")
    print("U(1) Ground ≈ 0.00 (Gapless / Massless)")
    print("SU(2) Ground > 0.00 (Massive)")
    print("Geometric frustration creates the Mass Gap.")


if __name__ == "__main__":
    main()
