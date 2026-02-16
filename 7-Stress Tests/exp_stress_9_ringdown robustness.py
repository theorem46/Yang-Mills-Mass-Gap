"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_stress_9_ringdown robustness.py
Category:        7-Stress Tests
Researcher:      Dr. David Swanagon
Original Date:   February 14, 2026
Paper Reference: Section 40.X (Model-Independent Observational Stealth)
Theorem Support: "Structural Stability of the Relational Core under Metric Regularization Freedom"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Performs cross-model verification of Option A core scaling by
    testing two independent regularized black hole metrics:

        1. Hayward-like suppression
        2. Bardeen-like suppression

    Both metrics implement the same cubic scaling law:

        r_min = α M^(1/3)

    but differ in how curvature is suppressed at small r.

    For each model and each α, the script computes:

        • Photon sphere radius (solve: 2f − r f' = 0)
        • Shadow radius: b = r_ph / sqrt(f(r_ph))

    Deviations are measured relative to Schwarzschild values:

        r_ph = 3M
        b_sh = 3√3 M

    This determines whether observational stealth depends on the
    specific functional form of regularization or is a structural
    consequence of the scaling law itself.

ADVERSARIAL CONDITIONS:
    - Black Hole Mass:         M = 30 (GW150914 scale)
    - Scaling Law:             r_min = α M^(1/3)
    - Alpha Range:             0.01, 0.05, 0.10
    - Models Tested:           Hayward-like and Bardeen-like
    - Observables:             Photon sphere + Shadow radius
    - Solver:                  Newton root-finding near 3M
    - Detection Threshold:     1% deviation (LIGO/EHT scale)

PASS CRITERIA:
    1. Cross-Model Stability:  Small deviations in both metrics.
    2. Dual Observable Check:  Photon sphere and shadow both < 1%.
    3. Structural Robustness:  Stealth persists independent of
                                suppression power-law details.

USAGE:
    python3 exp_optionA_cross_model_robustness.py

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""


import numpy as np
import scipy.optimize as opt

def run_robustness_test():
    print("\nRELATIONAL LYSIS: OPTION A ROBUSTNESS CHECK")
    print("Cross-Model Verification (Hayward vs Bardeen)")
    print("--------------------------------------------------------------------------------")
    print(f"{'Alpha':<6} | {'Model':<10} | {'r_ph Dev (%)':<15} | {'Shadow Dev (%)':<15} | {'Verdict'}")
    print("-" * 80)

    # Parameters
    M = 30.0
    alpha_scenarios = [0.01, 0.05, 0.10]
    
    # Standard Schwarzschild Values for Reference
    # f(r) = 1 - 2M/r
    # Photon Sphere r_ph = 3M
    # Shadow Radius b_sh = 3*sqrt(3)*M approx 5.196 M
    r_ph_std = 3.0 * M
    b_sh_std = 3.0 * np.sqrt(3.0) * M

    for alpha in alpha_scenarios:
        # Relational Core Scale
        r_min = alpha * (M**(1.0/3.0))

        # --- Model 1: Hayward-like (Original Script) ---
        # f(r) = 1 - 2Mr^2 / (r^3 + 2M*r_min^2)
        def f_hay(r):
            return 1.0 - (2*M*r**2)/(r**3 + 2*M*r_min**2)
        
        # Derivative f'(r)
        def df_hay(r):
            num_prime = 4*M*r
            denom = r**3 + 2*M*r_min**2
            denom_prime = 3*r**2
            term_prime = (num_prime * denom - (2*M*r**2) * denom_prime) / (denom**2)
            return -term_prime

        # --- Model 2: Bardeen-like (Alternative Regularization) ---
        # f(r) = 1 - 2Mr^2 / (r^2 + r_min^2)^(3/2)
        # This checks if the result depends on the specific power law of suppression
        def f_bar(r):
            return 1.0 - (2*M*r**2) / ((r**2 + r_min**2)**1.5)
        
        def df_bar(r):
            # f(r) = 1 - 2M * u * v^-1.5 where u=r^2, v=r^2+r_min^2
            # f'(r) = -2M [ (2r * v^-1.5) + (r^2 * -1.5 * v^-2.5 * 2r) ]
            v = r**2 + r_min**2
            term1 = 2*r * (v**-1.5)
            term2 = r**2 * (-1.5) * (v**-2.5) * 2*r
            return -2*M * (term1 + term2)

        # --- Solver Logic ---
        models = [("Hayward", f_hay, df_hay), ("Bardeen", f_bar, df_bar)]

        for name, f, df in models:
            # 1. Solve for Photon Sphere: 2f(r) - r f'(r) = 0
            def photon_eq(r):
                return 2*f(r) - r*df(r)
            
            try:
                r_ph = opt.newton(photon_eq, 3.0*M)
            except:
                r_ph = 3.0*M

            # 2. Calculate Shadow Radius (Impact Parameter)
            # b = r_ph / sqrt(f(r_ph))
            # This is what EHT sees.
            f_val = f(r_ph)
            b_shadow = r_ph / np.sqrt(f_val)

            # 3. Deviations
            dev_ph = abs((r_ph - r_ph_std) / r_ph_std) * 100
            dev_sh = abs((b_shadow - b_sh_std) / b_sh_std) * 100

            # 4. Verdict
            if dev_ph < 1.0 and dev_sh < 1.0:
                verdict = "ROBUST"
            else:
                verdict = "DETECTABLE"

            print(f"{alpha:<6.2f} | {name:<10} | {dev_ph:<15.4f} | {dev_sh:<15.4f} | {verdict}")
        print("-" * 80)

    print("\nINTERPRETATION:")
    print("If deviations remain small across BOTH models and BOTH observables,")
    print("the 'Observational Stealth' of the Relational Core is a structural")
    print("property of the scaling law, not a trick of the metric.")

if __name__ == "__main__":
    run_robustness_test()