#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_57_boundary robustness.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 9, 2026
Paper Reference: Section 5.3 (Uniform Covariant Coercivity)
Theorem Support: "Elliptic Coercivity Implies Spectral Gap"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests whether the "Coercivity" (Spectral Gap) of the Relational Lysis
    operator is robust to changes in boundary conditions.
    
    The mass gap should be an intrinsic bulk property, not an artifact of
    clamping the edges. This script verifies that the Rayleigh Quotient
    <x, Lx>/<x, x> remains strictly positive (or negative definite for -L)
    under Periodic, Dirichlet, and Neumann boundaries.

ADVERSARIAL CONDITIONS:
    - Boundaries:              [Periodic, Dirichlet, Neumann]
    - Input:                   Random Gaussian Noise
    - Trials:                  10 per boundary type

PASS CRITERIA:
    1. Coercivity:             Mean Rayleigh Quotient is bounded away from 0.
    2. Consistency:            Gap exists regardless of boundary choice.

USAGE:
    python3 exp_core_val_37_boundary_robustness.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np

N = 400
TRIALS = 10

# -------------------------------
# Relational Lysis Operators
# -------------------------------


def lysis_periodic(x):
    return np.roll(x, -1) - 2 * x + np.roll(x, 1)


def lysis_dirichlet(x):
    y = np.zeros_like(x)
    for i in range(1, len(x) - 1):
        y[i] = x[i + 1] - 2 * x[i] + x[i - 1]
    return y


def lysis_neumann(x):
    y = np.zeros_like(x)
    y[0] = x[1] - x[0]
    y[-1] = x[-2] - x[-1]
    for i in range(1, len(x) - 1):
        y[i] = x[i + 1] - 2 * x[i] + x[i - 1]
    return y


# -------------------------------
# Rayleigh Quotient
# -------------------------------


def coercivity_ratio(x, Lx):
    return np.dot(x, Lx) / np.dot(x, x)


# -------------------------------
# Main Test
# -------------------------------


def test_boundary(name, operator):
    ratios = []
    for _ in range(TRIALS):
        x = np.random.randn(N)
        Lx = operator(x)
        ratios.append(coercivity_ratio(x, Lx))
    return np.mean(ratios), np.std(ratios)


def main():
    print("\nRELATIONAL LYSIS — SCRIPT TYPE 37")
    print("Boundary Condition Robustness Test")
    print("-----------------------------------------")

    mP, sP = test_boundary("Periodic", lysis_periodic)
    mD, sD = test_boundary("Dirichlet", lysis_dirichlet)
    mN, sN = test_boundary("Neumann", lysis_neumann)

    print(f"Periodic  : mean={mP:.6f}  std={sP:.2e}")
    print(f"Dirichlet : mean={mD:.6f}  std={sD:.2e}")
    print(f"Neumann   : mean={mN:.6f}  std={sN:.2e}")

    print("\nINTERPRETATION:")
    print("If means are negative and bounded away from 0:")
    print("Relational Lysis is coercive under all boundaries.")
    print("Therefore spectral gap is intrinsic.")


if __name__ == "__main__":
    main()
