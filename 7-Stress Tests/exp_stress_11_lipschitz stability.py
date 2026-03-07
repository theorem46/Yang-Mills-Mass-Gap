"""
RELATIONAL LYSIS — REPRESENTATION LIPSCHITZ TEST
Tier-1 Non-Degenerate Validation (Interpolation Operator)

Purpose
-------
Test Lipschitz continuity of representation Φ using a
non-identity interpolation operator consistent with Appendix A.

Mathematical Form
-----------------
Φ(S) = Smooth( ∇S )

Test:
||Φ(S+δ) − Φ(S)|| ≤ C ||S||_RL
"""

import numpy as np
import time


# ============================================================
# RL Norm  ||∇S||
# ============================================================

def rl_norm(u, dx):
    grad = np.gradient(u, dx)
    return np.sqrt(np.sum(grad**2) * dx)


# ============================================================
# L2 Norm
# ============================================================

def l2_norm(u, dx):
    return np.sqrt(np.sum(u**2) * dx)


# ============================================================
# Stable Interpolation Operator  I_h
# (Gaussian smoothing kernel)
# ============================================================

def smooth(u, sigma=2.0):
    """
    Stable smoothing operator approximating FEM interpolation.
    """
    radius = int(3 * sigma)
    x = np.arange(-radius, radius + 1)

    kernel = np.exp(-(x**2) / (2 * sigma**2))
    kernel /= np.sum(kernel)

    return np.convolve(u, kernel, mode="same")


# ============================================================
# Representation Φ = I_h(∇S)
# ============================================================

def phi_map(S, dx):
    grad = np.gradient(S, dx)
    interp = smooth(grad, sigma=2.0)
    return interp


# ============================================================
# Lipschitz Trial
# ============================================================

def lipschitz_trial(n, deltas, trials):

    dx = 1.0 / (n - 1)
    ratios = []

    for _ in range(trials):

        S = np.random.randn(n)

        for d in deltas:

            perturb = np.random.randn(n)
            perturb /= np.linalg.norm(perturb)

            S2 = S + d * perturb

            phi1 = phi_map(S, dx)
            phi2 = phi_map(S2, dx)

            numerator = l2_norm(phi2 - phi1, dx)
            denominator = rl_norm(S2 - S, dx)

            ratios.append(numerator / denominator)

    return np.array(ratios)


# ============================================================
# Experiment Runner
# ============================================================

def run():

    print("\n====================================================")
    print("RELATIONAL LYSIS — REPRESENTATION LIPSCHITZ TEST")
    print("Tier-1 Non-Degenerate Version")
    print("====================================================\n")

    start = time.time()

    deltas = np.logspace(-7, -1, 12)
    resolutions = [128, 256, 512, 1024]

    means = []

    for n in resolutions:

        ratios = lipschitz_trial(n, deltas, trials=20)

        mean = np.mean(ratios)
        std = np.std(ratios)

        means.append(mean)

        print(f"\nResolution n = {n}")
        print(f"Mean Lipschitz Constant : {mean:.6f}")
        print(f"Std Dev                 : {std:.6f}")
        print(f"Min / Max               : {ratios.min():.6f} / {ratios.max():.6f}")

    means = np.array(means)

    slope = np.polyfit(resolutions, means, 1)[0]

    print("\n====================================================")
    print("RESOLUTION INDEPENDENCE ANALYSIS")
    print("====================================================")

    print("Means:", means)
    print("Slope:", slope)

    if abs(slope) < 1e-3:
        print("PASS: Resolution-independent Lipschitz constant")
    else:
        print("WARNING: Resolution dependence detected")

    print("\nTotal Time:", time.time() - start, "sec")
    print("====================================================\n")


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    run()