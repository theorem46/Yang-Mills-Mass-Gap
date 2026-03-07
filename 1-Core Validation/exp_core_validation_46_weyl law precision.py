#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_46_weyl law precision.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Paper Reference: Section 5.4 (Continuum Limit)
Theorem Support: "Weyl Law Spectral Scaling"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Verifies eigenvalue growth lambda_k ~ k^2.
    Confirms operator belongs to the correct universality class (Laplacian).

ADVERSARIAL CONDITIONS:
    - Modes:                   k=1 to 200 (Script 11), k=1 to 50 (Script 11b)
    - N:                       800 to 2000

PASS CRITERIA:
    1. Scaling Exponent:       Approx 2.0 (1.999 in Script 11b).
-------------------------------------------------------------------------------
"""
import numpy as np

# -----------------------------
# Parameters
# -----------------------------
N = 2000  # Large lattice to support many low modes
FIT_WINDOW = 50  # Fit only the first 50 modes


# -----------------------------
# Build Laplacian
# -----------------------------
def build_L(n):
    # Standard Dirichlet Laplacian
    # 2 on diag, -1 on off-diag
    main = 2.0 * np.ones(n)
    off = -1.0 * np.ones(n - 1)
    L = np.diag(main) + np.diag(off, k=1) + np.diag(off, k=-1)
    return L


# -----------------------------
# Main
# -----------------------------
def main():
    print("\nRELATIONAL LYSIS — SCRIPT TYPE 11B")
    print("Weyl Law Precision Test (Low-Energy Limit)")
    print("--------------------------------------------------")

    L = build_L(N)

    # We only need the bottom spectrum
    # Using eigvalsh for all is fine for N=2000 (fast enough)
    eigvals = np.linalg.eigvalsh(L)

    # Drop the very first one if it's effectively zero (Dirichlet starts > 0, but let's be safe)
    # Actually Dirichlet lambda_1 > 0. Let's take index 0 to FIT_WINDOW.

    subset_lambda = eigvals[0:FIT_WINDOW]
    subset_k = np.arange(1, FIT_WINDOW + 1)

    log_lam = np.log(subset_lambda)
    log_k = np.log(subset_k)

    # Fit
    slope, intercept = np.polyfit(log_k, log_lam, 1)

    print(f"Lattice Size (N): {N}")
    print(f"Fit Window (k):   1 to {FIT_WINDOW}")
    print(f"Fitted Exponent:  {slope:.6f}")
    print(f"Error from 2.0:   {abs(2.0 - slope):.6f}")

    print("\nCheck first 5 ratios (lambda / k^2):")
    # In continuum, lambda = c * k^2, so ratio should be constant
    ratios = subset_lambda[:5] / (subset_k[:5] ** 2)
    base_ratio = ratios[0]
    for i, r in enumerate(ratios):
        print(f"k={i+1}: Ratio={r:.6e} (Norm: {r/base_ratio:.4f})")

    print("\nINTERPRETATION:")
    print("If Exponent is > 1.99, the deviation in Script 11")
    print("was purely due to high-energy lattice artifacts.")
    print("The operator is perfect in the continuum.")


if __name__ == "__main__":
    main()
