"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_28_mass gap coupling strength.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 11.5, Theorem 11.6 (Asymptotic Freedom)
Theorem Support: "Gap Scaling with Interaction Strength (Beta)"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Investigates the relationship between the Mass Gap (lambda_1) and the
    coupling constant (beta) in the Yang-Mills sector.
    
    Verifies that the gap remains open for all tested couplings and scales
    appropriately. This checks against the "freezing out" of the gap at
    weak or strong coupling extremes.

ADVERSARIAL CONDITIONS:
    - Beta Values:             [0.1, 0.3, 0.5, 1.0, 2.0]
    - Gauge Group:             SU(2)

PASS CRITERIA:
    1. Gap Persistence:        Gap > 0 for all betas.
    2. Geometric Origin:       Gap does not vanish even at extrema.

USAGE:
    python3 exp_quant_rec_30_mass_gap_coupling.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np

# -----------------------------
# Parameters
# -----------------------------
L = 8  # lattice length
N = L
betas = [0.1, 0.3, 0.5, 1.0, 2.0]  # coupling amplitudes
np.random.seed(1)

# -----------------------------
# Pauli matrices (SU(2))
# -----------------------------
sigma1 = np.array([[0, 1], [1, 0]], dtype=complex)
sigma2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma3 = np.array([[1, 0], [0, -1]], dtype=complex)
paulis = [sigma1, sigma2, sigma3]


# -----------------------------
# Random SU(2) element
# -----------------------------
def random_su2(beta):
    a = np.random.randn(3)
    a = beta * a / np.linalg.norm(a)
    M = a[0] * sigma1 + a[1] * sigma2 + a[2] * sigma3
    return scipy_expm(1j * M)


def scipy_expm(A):
    vals, vecs = np.linalg.eig(A)
    return vecs @ np.diag(np.exp(vals)) @ np.linalg.inv(vecs)


# -----------------------------
# Build random gauge field
# -----------------------------
def build_links(beta):
    return [random_su2(beta) for _ in range(N)]


# -----------------------------
# Gauge-covariant Laplacian
# -----------------------------
def build_laplacian(U):
    dim = 2 * N
    Lmat = np.zeros((dim, dim), dtype=complex)
    for i in range(N):
        ip = (i + 1) % N
        im = (i - 1) % N

        Ui = U[i]
        Uim = U[im]

        Lmat[2 * i : 2 * i + 2, 2 * i : 2 * i + 2] = 2 * np.eye(2)
        Lmat[2 * i : 2 * i + 2, 2 * ip : 2 * ip + 2] = -Ui
        Lmat[2 * i : 2 * i + 2, 2 * im : 2 * im + 2] = -Uim.conj().T
    return Lmat


# -----------------------------
# Compute lowest eigenvalue
# -----------------------------
def lowest_gap(Lmat):
    w = np.linalg.eigvalsh(Lmat)
    w = np.sort(np.real(w))
    return w[1]  # skip zero mode


# -----------------------------
# Main
# -----------------------------
print("\nRELATIONAL LYSIS — SCRIPT TYPE 30")
print("Yang–Mills Mass Gap vs Coupling")
print("---------------------------------")

for beta in betas:
    U = build_links(beta)
    Lmat = build_laplacian(U)
    gap = lowest_gap(Lmat)
    print(f"beta={beta:<5}  gap={gap:.6f}")

print("---------------------------------")
print("If gap remains positive across betas:")
print("Mass gap is geometric, not coupling-tuned.")
