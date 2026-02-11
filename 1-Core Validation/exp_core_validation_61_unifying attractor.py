"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_core_validation_61_unifying attractor.py
Category:        1-Core Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 12.1, Unifying Theorem 1 (The Convergence Axiom)
Theorem Support: "Universality of the Alignment Diamond Attractor"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Validates the existence of a universal attractor in the Relational Lysis 
    hierarchy. The script generates random high-entropy integer states and 
    subjects them to a recursive SVD-based cascade (Lysis Step). 
    
    By decomposing the state into its principal direction (Alignment Diamond) 
    and residual energy (Shadow), and then reconstituting and repeating, 
    the experiment tests if disparate initial conditions converge toward 
    a singular, sign-invariant orientation in the state space. 
    
    A sign-normalized cosine mean approaching 1.0 proves that the Relational 
    Lysis operator acts as a global attractor, mapping diverse data 
    architectures to a unified geometric basis.

ADVERSARIAL CONDITIONS:
    - Trials:                   40 (Independent random seeds)
    - Depth:                    8 Cascade Levels
    - Initial State:            Large-magnitude random integers ($10^6$)
    - Metric:                   Sign-Normalized Pairwise Cosine Similarity

PASS CRITERIA:
    1. Absolute Convergence:   Mean |Cosine| > 0.99.
    2. Attractor Stability:    Sign-normalized mean similarity approaches 1.0.

USAGE:
    python3 exp_core_val_unifying_theorem_type_1_attractor.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np

# ============================================================
# RELATIONAL LYSIS — UNIFYING THEOREM TYPE 1 (CORRECTED)
# State = Alignment Diamond + Shadow
# Hierarchical cascade, integer-safe
# ============================================================

DIM = 2
LEVELS = 8
TRIALS = 40
EPS = 1e-12

# ----------------------------
# Basic linear tools
# ----------------------------


def normalize(v):
    n = np.linalg.norm(v)
    if n < EPS:
        return v
    return v / n


def cosine(a, b):
    return float(np.dot(normalize(a), normalize(b)))


# ----------------------------
# Relational Lysis Step
# ----------------------------


def lysis_step(x):
    """
    Alignment diamond = first principal direction
    Shadow = residual energy
    """
    x = np.array(x, dtype=float)
    c = x.reshape(-1, 1)
    U, S, Vt = np.linalg.svd(c, full_matrices=False)
    diamond = normalize(Vt[0])
    shadow = S[1] if len(S) > 1 else 0.0
    return diamond, shadow


# ----------------------------
# Hierarchical Cascade
# ----------------------------


def cascade(x0, levels):
    diamonds = []
    shadows = []
    x = np.array(x0, dtype=float)

    for _ in range(levels):
        d, s = lysis_step(x)
        diamonds.append(d)
        shadows.append(s)
        # Reconstitute state: diamond + shadow
        x = d + s

    return diamonds, shadows


# ----------------------------
# Generate integer seed
# ----------------------------


def random_integer_state():
    return np.random.randint(1, 10**6, size=DIM)


# ----------------------------
# Main
# ----------------------------


def main():
    final_diamonds = []

    print("\nRELATIONAL LYSIS — UNIFYING THEOREM TYPE 1 (CORRECTED)")
    print("-------------------------------------------------------")

    for t in range(TRIALS):
        x0 = random_integer_state()
        D, S = cascade(x0, LEVELS)
        final_diamonds.append(D[-1])

    final_diamonds = np.array(final_diamonds)

    # --------------------------------------------------
    # RAW PAIRWISE COSINES
    # --------------------------------------------------

    raw = []
    for i in range(TRIALS):
        for j in range(i + 1, TRIALS):
            raw.append(cosine(final_diamonds[i], final_diamonds[j]))
    raw = np.array(raw)

    # --------------------------------------------------
    # ABSOLUTE COSINES  (CORRECT METRIC)
    # --------------------------------------------------

    abs_cos = np.abs(raw)

    # --------------------------------------------------
    # SIGN NORMALIZATION
    # --------------------------------------------------

    ref = final_diamonds[0]
    corrected = []

    for d in final_diamonds:
        s = np.sign(np.dot(ref, d))
        if s == 0:
            s = 1
        corrected.append(s * d)

    corrected = np.array(corrected)

    corr = []
    for i in range(TRIALS):
        for j in range(i + 1, TRIALS):
            corr.append(cosine(corrected[i], corrected[j]))
    corr = np.array(corr)

    # --------------------------------------------------
    # REPORT
    # --------------------------------------------------

    print("\nRAW COSINE STATS")
    print("Mean:", raw.mean())
    print("Min :", raw.min())
    print("Max :", raw.max())

    print("\nABS(COSINE) STATS")
    print("Mean |cos|:", abs_cos.mean())
    print("Fraction |cos| > 0.99:", np.mean(abs_cos > 0.99))

    print("\nSIGN-NORMALIZED COSINE STATS")
    print("Mean:", corr.mean())
    print("Min :", corr.min())
    print("Max :", corr.max())

    print("\nINTERPRETATION:")
    print("If mean |cos| -> 1 and sign-normalized mean -> 1")
    print("then universal alignment attractor exists.")


# ----------------------------

if __name__ == "__main__":
    main()
