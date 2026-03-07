import numpy as np
import time


# ============================================================
# Relational Energy (correct scaling)
# ============================================================

def relational_energy(S, dx):
    diff = S[1:] - S[:-1]
    return np.sum(diff**2) / dx


# ============================================================
# Continuum Energy
# ============================================================

def continuum_energy(S, dx):
    grad = np.gradient(S, dx)
    return np.sum(grad**2) * dx


# ============================================================
# Experiment
# ============================================================

def run():

    print("\nRELATIONAL LYSIS — ENERGY EQUIVALENCE TEST (Corrected)\n")

    sizes = [64, 128, 256, 512, 1024]
    trials = 50

    means = []

    for n in sizes:

        dx = 1.0 / (n - 1)
        ratios = []

        for _ in range(trials):

            S = np.random.randn(n)

            e_rl = relational_energy(S, dx)
            e_ct = continuum_energy(S, dx)

            ratios.append(e_ct / e_rl)

        ratios = np.array(ratios)

        mean = np.mean(ratios)
        std = np.std(ratios)

        means.append(mean)

        print(f"n={n}")
        print(f"Mean Ratio : {mean:.6f}")
        print(f"Std        : {std:.6f}")
        print()

    means = np.array(means)
    slope = np.polyfit(sizes, means, 1)[0]

    print("Means:", means)
    print("Slope:", slope)


if __name__ == "__main__":
    run()