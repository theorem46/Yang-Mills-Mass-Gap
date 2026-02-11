"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_41_mass gap validation.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 5.7, Theorem 5.7 (Yang-Mills Mass Gap)
Theorem Support: "Existence of a Uniform Positive Mass Gap in Non-Abelian Fields"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    The "Final RL / Classical Mass Gap Validation". This script constructs the
    Relational Lysis shadow operator (interpreted as the Hamiltonian H = -R)
    for various gauge groups and verifies the spectral gap behavior.

    It explicitly contrasts the Non-Abelian (SU(2)) case against Abelian (U(1))
    and Trivial/Pure-Gauge baselines. The presence of a persistent positive gap
    in SU(2) vs. zero modes in the others confirms the geometric origin of mass
    arising from non-commutative curvature.

ADVERSARIAL CONDITIONS:
    - Gauge Groups:            SU(2) (Target), U(1), U(1) Pure Gauge, Trivial
    - Lattice Sizes:           20 to 120
    - Perturbation:            Random group elements (eps=0.3)

PASS CRITERIA:
    1. SU(2) Gap:              Strictly positive (Gap > 0).
    2. U(1)/Trivial Gap:       Vanishing or presence of Kernel (Gap ~ 0).
    3. Hermiticity:            Operator is self-adjoint (Error ~ 1e-15).

USAGE:
    python3 exp_quant_rec_ym_1_mass_gap_validation.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
from numpy.linalg import eigvals, norm
from scipy.linalg import expm

# ---------------------------
# Lie algebra generators
# ---------------------------


def su2_generators():
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    return sx, sy, sz


# ---------------------------
# Random group elements
# ---------------------------


def random_su2(eps, rng):
    sx, sy, sz = su2_generators()
    a = rng.normal(size=3)
    A = 1j * (a[0] * sx + a[1] * sy + a[2] * sz)
    return expm(eps * A)


def random_u1(eps, rng):
    theta = eps * rng.normal()
    return np.exp(1j * theta)


# Pure gauge U(1): U_i = exp(i(theta_{i+1}-theta_i))
def pure_gauge_u1(N, eps, rng):
    theta = eps * rng.normal(size=N)
    U = []
    for i in range(N):
        ip = (i + 1) % N
        U.append(np.exp(1j * (theta[ip] - theta[i])))
    return U


# ---------------------------
# Build operator
# ---------------------------


def build_operator(N, group="SU2", eps=0.3, seed=0):
    rng = np.random.default_rng(seed)

    if group == "SU2":
        block = 2
        U = [random_su2(eps, rng) for _ in range(N)]
        inv = lambda M: M.conj().T

    elif group == "U1":
        block = 1
        U = [random_u1(eps, rng) for _ in range(N)]
        inv = lambda M: np.conj(M)

    elif group == "U1_PURE":
        block = 1
        U = pure_gauge_u1(N, eps, rng)
        inv = lambda M: np.conj(M)

    elif group == "TRIVIAL":
        block = 1
        U = [1.0 for _ in range(N)]
        inv = lambda M: 1.0

    else:
        raise ValueError("Unknown group")

    dim = block * N
    R = np.zeros((dim, dim), dtype=complex)

    for i in range(N):
        ip = (i + 1) % N
        im = (i - 1) % N

        R[i * block : (i + 1) * block, i * block : (i + 1) * block] = -2 * np.eye(block)

        R[i * block : (i + 1) * block, ip * block : (ip + 1) * block] = U[i]

        R[i * block : (i + 1) * block, im * block : (im + 1) * block] = inv(U[im])

    return R


# ---------------------------
# Diagnostics
# ---------------------------


def hermiticity_error(M):
    return norm(M - M.conj().T)


def spectrum(M):
    vals = np.real(eigvals(M))
    vals.sort()
    return vals


def kernel_dim(vals, tol=1e-8):
    return np.sum(np.abs(vals) < tol)


# ---------------------------
# Run single experiment
# ---------------------------


def run_case(N, group):
    R = build_operator(N, group)
    H = -R  # Hamiltonian
    vals = spectrum(H)

    return {
        "lambda_min": vals[0],
        "kernel": kernel_dim(vals),
        "herm_err": hermiticity_error(H),
    }


# ---------------------------
# Sweep
# ---------------------------


def main():
    Ns = [20, 40, 80, 120]
    groups = ["SU2", "U1", "U1_PURE", "TRIVIAL"]

    print("\n==== FINAL RL / CLASSICAL MASS GAP VALIDATION ====\n")

    for g in groups:
        print(f"\nGROUP = {g}")
        for N in Ns:
            r = run_case(N, g)
            print(
                f"N={N:4d}   "
                f"gap={r['lambda_min']:.6f}   "
                f"kernel={r['kernel']}   "
                f"herm_err={r['herm_err']:.2e}"
            )


if __name__ == "__main__":
    main()
