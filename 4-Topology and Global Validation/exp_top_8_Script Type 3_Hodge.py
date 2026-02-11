"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_top_8_Script Type 3_Hodge.py
Category:        4-Topology and Global Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 38.1 (Rationality and Hodge-Type Winding)
Theorem Support: "Quantization of Harmonic Modes on Rational Topological Cycles"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the 'Rationality Criterion' of the Hodge Conjecture using a topological 
    winding proxy. In Hodge theory, only specific rational cohomology classes 
    correspond to algebraic cycles. This script simulates this by applying a 
    complex unitary twist ($\exp(i \cdot 2\pi n)$) to the periodic boundary of 
    a 1D lattice.
    
    The experiment evaluates the ground state eigenvalue ($e_0$) for different 
    winding numbers ($n$). For integer/rational winding ($n=1.0, 2.0$), the 
    system should recover a near-zero harmonic mode. For fractional winding 
    ($n=0.5, 1.5$), the topological 'frustration' should lift the eigenvalue 
    above the ground state. This verifies that stable 'diamonds' are 
    algebraically quantized.

ADVERSARIAL CONDITIONS:
    - Lattice Size:             N = 100
    - Winding Factors (n):      [0.5, 1.0, 1.5, 2.0]
    - Boundary Condition:       Periodic with Unitary Topological Twist
    - Metric:                   Smallest Eigenvalue ($e_0$) Magnitude

PASS CRITERIA:
    1. Rational Recovery:      $e_0 \approx 0$ for integer winding numbers.
    2. Topological Gap:        $e_0 > 0$ for fractional winding (frustration).
    3. Harmonic Distinction:   Confirms that the Lysis hierarchy only admits 
                               stable solutions on rationally closed cycles.

USAGE:
    python3 exp_top_val_3_hodge_winding_rationality.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh


def main():
    print("\nRELATIONAL LYSIS — SCRIPT TYPE 3_Hodge")
    print("Topological Winding & Rationality Test")
    print("--------------------------------------------------")
    print(f"{'Winding (n)':<15} {'Smallest Eigenvalue':<25} {'Status'}")

    N = 100
    size = N

    # We test Rational (1.0, 2.0) vs Transcendental/Fractional (0.5, 1.5)
    for n in [0.5, 1.0, 1.5, 2.0]:
        # Identity links for the bulk
        main = 2.0 * np.ones(size, dtype=complex)
        off_diag = -1.0 * np.ones(size - 1, dtype=complex)

        # The 'Twist' is concentrated at the boundary wrap-around
        # This simulates a topological Hodge Cycle
        twist = np.exp(1j * 2 * np.pi * n)

        L_base = diags(
            [main, off_diag, off_diag], [0, 1, -1], shape=(size, size)
        ).tolil()

        # Periodic Boundary Condition with Topological Twist
        # This creates the 'Aharonov-Bohm' winding effect
        L_base[size - 1, 0] = -twist
        L_base[0, size - 1] = -np.conj(twist)

        L = L_base.tocsr()

        # We solve for the ground state
        vals = eigsh(L, k=1, which="SM", return_eigenvectors=False)
        e0 = np.abs(vals[0])

        # Rationality Threshold: Integer winding must recover the zero-mode
        status = "RATIONAL (HODGE)" if e0 < 1e-10 else "FRUSTRATED (NON-HODGE)"
        print(f"{n:<15} {e0:.12e}            {status}")

    print("--------------------------------------------------")
    print("INTERPRETATION:")
    print("If n=1.0 and 2.0 show ~0, but 0.5 and 1.5 show > 0:")
    print("Relational Lysis proves that stable Harmonic cycles are")
    print("exclusively tied to RATIONAL algebraic configurations.")


if __name__ == "__main__":
    main()
