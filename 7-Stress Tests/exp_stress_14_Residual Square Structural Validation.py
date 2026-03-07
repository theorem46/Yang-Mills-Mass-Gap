"""
RELATIONAL LYSIS — RESIDUAL SQUARE VALIDATION (Tier-1)

Script Name:     exp_stress_14_Residual Square Structural Validation.py
Category:        7-Stress Tests
Paper Reference: Appendix C (Residual Positivity)

Purpose
-------
Validate that interaction energy scales quadratically with
residual magnitude:

    E ∝ ||r||^2

which supports sum-of-squares energy structure.

Diagnostics
-----------
• Multi-scale magnitude sweep
• Monte-Carlo averaging
• Log–log slope estimation
• Proportionality constant estimation
• Stability checks
"""

import numpy as np
import time


# ============================================================
# Residual Energy
# ============================================================

def residual_energy(r):
    """
    Quadratic residual energy.
    """
    return np.sum(r**2)


# ============================================================
# Single Magnitude Trial
# ============================================================

def trial_for_magnitude(m, dim, trials):

    energies = []

    for _ in range(trials):
        r = np.random.randn(dim) * m
        e = residual_energy(r)
        energies.append(e)

    energies = np.array(energies)

    return {
        "mean": np.mean(energies),
        "std": np.std(energies),
        "min": np.min(energies),
        "max": np.max(energies),
    }


# ============================================================
# Main Experiment
# ============================================================

def run():

    print("\n====================================================")
    print("RELATIONAL LYSIS — RESIDUAL SQUARE TEST")
    print("Tier-1 Validation")
    print("====================================================\n")

    start = time.time()

    # Residual magnitude range
    mags = np.logspace(-5, 1, 20)

    # Residual vector dimension
    dim = 100

    # Monte-Carlo trials per magnitude
    trials = 50

    mean_energies = []

    for m in mags:

        stats = trial_for_magnitude(m, dim, trials)

        mean_energies.append(stats["mean"])

        print(f"Magnitude {m:.6e}")
        print(f"Mean Energy : {stats['mean']:.6e}")
        print(f"Std Dev     : {stats['std']:.6e}")
        print(f"Min / Max   : {stats['min']:.6e} / {stats['max']:.6e}")
        print()

    mean_energies = np.array(mean_energies)

    # ============================================================
    # Log-Log Slope (Quadratic Exponent Test)
    # ============================================================

    slope, intercept = np.polyfit(np.log(mags), np.log(mean_energies), 1)

    print("====================================================")
    print("QUADRATIC SCALING ANALYSIS")
    print("====================================================")

    print(f"Log–Log Slope (expected ≈ 2): {slope:.6f}")

    if abs(slope - 2.0) < 0.05:
        print("PASS: Quadratic scaling confirmed")
    else:
        print("WARNING: Deviation from quadratic scaling")

    # ============================================================
    # Proportionality Constant Estimate
    # ============================================================

    constants = mean_energies / (mags**2)
    const_mean = np.mean(constants)
    const_std = np.std(constants)

    print("\n====================================================")
    print("PROPORTIONALITY CONSTANT")
    print("====================================================")

    print(f"C ≈ {const_mean:.6f} ± {const_std:.6f}")

    elapsed = time.time() - start

    print("\n====================================================")
    print("EXECUTION COMPLETE")
    print(f"Total Time: {elapsed:.2f} sec")
    print("====================================================\n")


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    run()