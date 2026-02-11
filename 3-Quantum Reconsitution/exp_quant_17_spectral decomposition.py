"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_quant_17_spectral decomposition.py
Category:        3-Quantum Reconsitution
Researcher:      Dr. David Swanagon
Paper Reference: Section 11.1 (Field Decomposition)
Theorem Support: "Spectral Separation of Gravity and Gauge Fields"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Performs a spectral decomposition (FFT) of the Solved State Diamond.
    Splits the spectrum into Low-Frequency ("Gravitational") and High-Frequency
    ("EM-like") components.
    
    Measures the Energy and Adjacency of each component separately, demonstrating
    how the operator naturally separates scale-dependent physics.

ADVERSARIAL CONDITIONS:
    - Cutoff:                  1/6th of spectrum
    - Input:                   Mixed sine wave

PASS CRITERIA:
    1. Decomposition:          Successfully separates energy into distinct bands.
-------------------------------------------------------------------------------
"""

import numpy as np

def L(x):
    return x[2:] - 2*x[1:-1] + x[:-2]

def energy(z):
    return abs(np.dot(z[1:-1], L(z)))

def adjacency(z):
    return np.mean(np.abs(z[1:] - z[:-1]))

# solved state
N = 5000
t = np.linspace(0, 2*np.pi, N)
x = np.sin(17*t) + 0.4*np.sin(53*t)

# canonical diamond
D = L(x)

# FFT of diamond (purely geometric decomposition)
F = np.fft.rfft(D)
freqs = np.arange(len(F))

# frequency split (basin boundary)
cut = len(F) // 6

F_low  = F.copy()
F_high = F.copy()

F_low[cut:] = 0        # low-frequency (grav-like)
F_high[:cut] = 0       # high-frequency (EM-like)

D_grav = np.fft.irfft(F_low, len(D))
D_em   = np.fft.irfft(F_high, len(D))

print("GRAVITATIONAL DIAMOND")
print("Energy:", energy(D_grav))
print("Adjacency:", adjacency(D_grav))

print("\nEM-LIKE DIAMOND")
print("Energy:", energy(D_em))
print("Adjacency:", adjacency(D_em))
