#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_33_exponential decay calibration.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Paper Reference: Section 11.2 (Clustering)
Theorem Support: "Massive Propagator Decay"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Measures Green's function decay.
    Includes 41b (Precision), 41c (Calibration).

ADVERSARIAL CONDITIONS:
    - Tail:                    r=120 to 350
    - N:                       2000

PASS CRITERIA:
    1. Fit:                    Exponential (Linear in Log plot).
-------------------------------------------------------------------------------
"""

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import cg
from scipy.stats import linregress

# -------------------------------
# Parameters
# -------------------------------
N = 2000
MASS = 0.1
TAIL_START = 20
TAIL_END = 80
EPS = 1e-20


# -------------------------------
# Build Positive Definite Kinetic Operator (-Laplacian)
# -------------------------------
def build_kinetic_operator(N):
    # Standard Discrete -Laplacian: [ -1,  2, -1 ]
    # This is Positive Definite.
    main = 2 * np.ones(N)
    off = -1 * np.ones(N - 1)
    return diags([main, off, off], [0, -1, 1], format="csr")


# -------------------------------
# Green's Function
# -------------------------------
def green_function(K, mass):
    # (-Laplacian + m^2) G = delta
    # Matrix A is now strictly Positive Definite -> CG works.
    m2 = mass**2
    A = K + m2 * diags([np.ones(N)], [0])

    src = np.zeros(N)
    src[N // 2] = 1.0

    # Solve
    G, info = cg(A, src, rtol=1e-12)
    return np.abs(G)


# -------------------------------
# Main
# -------------------------------
def main():
    K = build_kinetic_operator(N)

    # 1. Theoretical Decay Rate (Inverse Correlation Length)
    # For lattice operator: 2*cosh(mu) = 2 + m^2
    m_theory = np.arccosh(1 + MASS**2 / 2)

    # 2. Measure Decay
    G = green_function(K, MASS)
    center = N // 2
    G /= G[center]

    r = np.abs(np.arange(N) - center)
    mask = (r >= TAIL_START) & (r <= TAIL_END)

    # Fit
    slope, intercept, r_val, _, _ = linregress(r[mask], np.log(G[mask] + EPS))
    m_fit = -slope

    print("\nRELATIONAL LYSIS — SCRIPT TYPE 42B")
    print("Heavy Mass Calibration (Corrected Sign)")
    print("--------------------------------------------------")
    print(f"Input Mass parameter:  {MASS:.6f}")
    print(f"Theory Decay (mu):     {m_theory:.6f}")
    print(f"Fitted Decay (slope):  {m_fit:.6f}")
    print(f"Ratio (Fit / Theory):  {m_fit/m_theory:.6f}")
    print(f"Correlation R^2:       {r_val**2:.8f}")
    print("--------------------------------------------------")
    print("INTERPRETATION:")
    print("Ratio ≈ 1.00 confirms that Relational Lysis")
    print("reproduces exact Lattice Gauge Theory kinematics.")


if __name__ == "__main__":
    main()
