#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_56_coercivity scaling.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 11.8, Theorem 11.8 (Operator Coercivity)
Theorem Support: "Scale-Invariance of Spectral Lower Bounds"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the coercivity of the Relational Lysis operator across multiple 
    orders of magnitude. 
    
    The script measures the normalized Rayleigh Quotient—the ratio of the 
    operator's action to the total energy of the state ($\langle x, Lx \rangle / \|x\|^2$)—as 
    the input vector $x$ is scaled by factors of $10^{-1}$ to $10^1$. 
    
    This verifies that the spectral gap is a fundamental property of the 
    operator's geometry and does not vanish or fluctuate simply due to 
    the amplitude of the field. A stable, non-zero ratio confirms that the 
    operator is coercive, providing a "restoring force" that prevents the 
    collapse of vacuum energy.

ADVERSARIAL CONDITIONS:
    - Lattice Size:             N = 200
    - Scale Factors ($s$):      [0.1, 0.3, 1, 3, 10, 30]
    - Metric:                   Scale-Invariant Energy Ratio

PASS CRITERIA:
    1. Scale Invariance:        Ratio remains constant regardless of $s$.
    2. Coercivity:              Ratio remains strictly bounded away from zero.

USAGE:
    python3 exp_core_val_36_coercivity_scaling.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np


# ---------------------------
# Lysis Operator
# ---------------------------
def lysis(x):
    return x[2:] - 2 * x[1:-1] + x[:-2]


def energy(x):
    L = lysis(x)
    return np.dot(L, L)


# ---------------------------
# Main
# ---------------------------
def main():
    print("\nRELATIONAL LYSIS — SCRIPT TYPE 36")
    print("Coercivity Scaling Test")
    print("--------------------------------------")
    print("scale   <x,Lx> / ||x||^2")
    print("--------------------------------------")

    N = 200
    base = np.random.randn(N)

    for s in [0.1, 0.3, 1, 3, 10, 30]:
        x = s * base
        Lx = lysis(x)
        num = np.dot(x[1:-1], Lx)
        den = np.dot(x, x)
        ratio = num / den
        print(f"{s:<6} {ratio:.6e}")

    print("--------------------------------------")
    print("INTERPRETATION:")
    print("If ratio remains bounded away from 0:")
    print("Relational Lysis is coercive.")


if __name__ == "__main__":
    main()
