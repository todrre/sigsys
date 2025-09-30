import control as ct
import matplotlib.pyplot as plt
import numpy as np

# Parametrar
G = 1
R = 1
C = 1
a = G / (R * C)

# Överföringsfunktioner
H_3 = ct.tf([1, 0, 0], [1, a, a**2])
H_2 = a * ct.tf([1, 0], [1, a, a**2])
H_1 = a ** 2 * ct.tf([1], [1, a, a**2])

systems = [H_3, H_2, H_1]
titles = ["H₃", "H₂", "H₁"]

# Skapa subplot: 3 rader x 3 kolumner
fig, axes = plt.subplots(3, 3, figsize=(15, 12))

# --- Rad 1: Pol–noll-diagram ---
for i, (sys, title) in enumerate(zip(systems, titles)):
    ct.pzmap(sys, plot=True, ax=axes[0, i])
    axes[0, i].set_title(f"Pol–noll karta för {title}")

# --- Rad 2: Impulssvar ---
for i, (sys, title) in enumerate(zip(systems, titles)):
    t, y = ct.impulse_response(sys)
    axes[1, i].plot(t, y)
    axes[1, i].grid(True)
    axes[1, i].set_title(f"Impulssvar för {title}")
    axes[1, i].set_xlabel("Tid [s]")
    axes[1, i].set_ylabel("Amplitude")

omega = np.logspace(-2, 2, 500)  # frekvensvektor

for i, (sys, title) in enumerate(zip(systems, titles)):
    s = 1j * omega                   # s = jω
    H_jw = sys(s)                    # beräkna H(jω)
    mag = 20 * np.log10(np.abs(H_jw))   # Magnitud i dB
    phase = np.angle(H_jw, deg=True)    # Fas i grader

    ax_mag = axes[2, i]                 # Magnitud-axeln
    ax_phase = ax_mag.twinx()           # Fas på andra y-axeln

    # Magnitud
    ax_mag.semilogx(omega, mag, 'b')
    ax_mag.set_ylabel("Magnitude [dB]", color='b')
    ax_mag.set_xlabel("Frekvens [rad/s]")
    ax_mag.grid(True, which="both")

    # Fas
    ax_phase.semilogx(omega, phase, 'r--')
    ax_phase.set_ylabel("Fas [°]", color='r')

    ax_mag.set_title(f"Bode-diagram för {title}")





plt.suptitle("Pol–noll-diagram, impulssvar och Bode-diagram för H₃, H₂ och H₁", fontsize=16)
plt.tight_layout()
plt.show()