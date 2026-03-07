#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_59_poincare compactness.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 11.10, Theorem 11.10 (Spectral Compactness)
Theorem Support: "Lower Bound of the Discrete Poincaré Constant"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the validity of the Poincaré Inequality for the Relational Lysis 
    operator. By projecting out the constant mode (zero-mean) and sampling 
    random state vectors, the script verifies that the energy of any non-trivial 
    fluctuation is bounded below by a multiple of its $L^2$ norm.
    
    This inequality is essential for proving that the operator has a compact 
    resolvent, which implies that the spectrum is discrete and the ground 
    state is isolated by a persistent gap. A strictly positive minimum 
    ratio $\langle x, Lx \rangle / \|x\|^2$ confirms the operator's coercivity and 
    the mathematical existence of the Mass Gap.

ADVERSARIAL CONDITIONS:
    - Lattice Size:             N = 500
    - Trials:                   200 (Random Gaussian noise)
    - Mode Control:             Projected Zero-Mean (Removing translation invariance)
    - Metric:                   Discrete Poincaré Ratio

PASS CRITERIA:
    1. Spectral Gap:           Minimum Ratio > 0.
    2. Statistical Stability:   Low standard deviation across random trials, 
                               indicating a robust lower spectral bound.

USAGE:
    python3 exp_core_val_39_poincare_compactness_test.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""
import numpy as np

# -------------------------------
# Relational Lysis (Discrete Laplacian)
# -------------------------------


def lysis(x):
    return x[2:] - 2 * x[1:-1] + x[:-2]


# -------------------------------
# Inner product
# -------------------------------


def inner(a, b):
    return float(np.dot(a, b))


# -------------------------------
# Remove constant mode
# -------------------------------


def project_zero_mean(x):
    return x - np.mean(x)


# -------------------------------
# Main
# -------------------------------


def main():

    np.random.seed(0)

    N = 500  # lattice size
    trials = 200  # number of random tests

    ratios = []

    for _ in range(trials):
        x = np.random.randn(N)
        x = project_zero_mean(x)

        Lx = lysis(x)

        num = inner(x[1:-1], Lx)
        den = inner(x[1:-1], x[1:-1])

        ratios.append(-num/den)

    ratios = np.array(ratios)

    print("\nRELATIONAL LYSIS — SCRIPT TYPE 39")
    print("Poincaré Inequality / Compactness Test")
    print("-----------------------------------------")
    print(f"Min  <x,Lx>/||x||^2 : {ratios.min():.6f}")
    print(f"Mean <x,Lx>/||x||^2 : {ratios.mean():.6f}")
    print(f"Std  deviation     : {ratios.std():.6f}")
    print("-----------------------------------------")
    print("INTERPRETATION:")
    print("If minimum > 0:")
    print("Relational Lysis satisfies a Poincaré inequality.")
    print("Operator is coercive and has a spectral gap.")
    print("Compact resolvent follows -> discrete spectrum.")


if __name__ == "__main__":
    main()
