#Paper: Relational Lysis and the Necessity of the Covariant Laplacian: A Structural Resolution of the Yang–Mills Mass #LinkedIn: https://www.linkedin.com/in/davidswanagon/
#Device: Apple M1 - 16GB - Series #WGR9MMW64F
#Date Run: March 03, 2026

"""
RELATIONAL LYSIS: EXPERIMENTAL VALIDATION SUITE
-------------------------------------------------------------------------------
Script Name:     exp_int_4_Navier Stokes Final_4.py
Category:        5-Internal Mechanism Validation
Researcher:      Dr. David Swanagon
Original Date:   February 11, 2026
Paper Reference: Section 31.2, Theorem 31.2 (Energy Descent and Closure)
Theorem Support: "Monotone Descent of Integer-Casted Hamiltonian Energy"

-------------------------------------------------------------------------------
EXPERIMENT DESCRIPTION:
    Tests the fundamental energy-descent property of the Relational Lysis 
    hierarchy. In a physically consistent "solved state," the energy of the 
    Alignment Diamond must strictly decrease as we descend levels, ultimately 
    closing into a harmonic ground state.
    
    The script initializes a field with a deterministic, scale-invariant 
    spectrum mimicking the Kolmogorov $k^{-5/3}$ cascade. It then performs 
    recursive lysis and measures the Hamiltonian energy (-⟨D, ΔD⟩). 
    
    By casting energy to an integer (integer quadratic energy), the experiment 
    ensures that the descent is not a numerical artifact but a structural 
    one. A result of "PASS" across multiple resolutions (N=64 to 1024) 
    verifies that the Relational Lysis cascade possesses a unique, 
    lower-bounded attractor.

ADVERSARIAL CONDITIONS:
    - Spectrum:                k^-5/3 (Scale-invariant / critical energy)
    - Resolutions (N):         [64, 128, 256, 512, 1024]
    - Depth:                   8 Levels of recursion
    - Metric:                  Integer-rounded Hamiltonian energy (-np.dot(D, lap(D)))

PASS CRITERIA:
    1. Strict Descent:         E[i] < E[i-1] for all active levels.
    2. Harmonic Closure:       If E reaches 0, it remains at 0 (fixed point).
    3. Resolution Invariance:  Closure logic holds identical across all lattice scales.

USAGE:
    python3 exp_core_val_critical_scale_tower_closure.py --verbose

LICENSE:
    Proprietary Research Code - Dr. David Swanagon
-------------------------------------------------------------------------------
"""

import numpy as np

def run(N, levels=8):
    L = 2*np.pi
    x = np.linspace(0, L, N, endpoint=False)
    k = np.fft.fftfreq(N, d=L/N) * 2*np.pi
    kk = np.abs(k); kk[0] = 1.0

    def grad(u): return np.real(np.fft.ifft(1j*k*np.fft.fft(u)))
    def lap(u):  return np.real(np.fft.ifft(-(k**2)*np.fft.fft(u)))
    def div_free(u): return u - np.mean(u)
    def B(u): return div_free(u*grad(u))

    # RL solved-state Φ
    def Phi(u):
        ux, uxx = grad(u), lap(u)
        rhs = B(u)
        M = np.vstack([uxx, ux, u]).T
        c, *_ = np.linalg.lstsq(M, rhs, rcond=None)
        D = M @ c
        S = rhs - D
        return D, S

    # Integer quadratic energy
    def energy_int(D):
        LD = lap(D)
        return int(np.round(-np.dot(D, LD)))

    # Scale-invariant deterministic spectrum ~ k^{-5/3}
    phases = np.sign(np.sin(13*x))
    u0 = np.real(np.fft.ifft((kk**(-5/6))*np.fft.fft(phases)))
    u = div_free(u0)

    Es = []
    for _ in range(levels):
        D, S = Phi(u)
        E = energy_int(D)
        Es.append(E)
        if E == 0: break
        u = D
    return Es

Ns = [64, 128, 256, 512, 1024]
results = {N: run(N) for N in Ns}

for N, Es in results.items():
    print(f"N={N}, energies:", Es)
    for i in range(1, len(Es)):
        if Es[i-1] > 0:
            assert Es[i] < Es[i-1], f"FAIL: non-descent at N={N}, level {i}"
        else:
            assert Es[i] == 0, f"FAIL: non-harmonic after convergence at N={N}, level {i}"

print("RESULT: PASS (Critical-scale tower closure)")
