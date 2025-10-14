import scipy.signal as signal
import matplotlib.pyplot as plt
import numpy as np

a = 40 # 600 * np.pi # Denna behöver räknas ut och är idag en gissning
b = 1 # 0.32 # Denna är uträknad 1 / (2 * c * np.sqrt(1 - c ** 2)), b = 2c

H_1 = signal.lti([0, 0, a**2], [1, b * a, a ** 2])
H_2 = signal.lti([0, a, 0], [1, b * a, a ** 2])
H_3 = signal.lti([1, 0, 0], [1, b * a, a ** 2])
systems = [H_1, H_2, H_3]
titles = ["H1-Lågpass", "H2-Bandpass", "H3-Högpass"]

fig, axes = plt.subplots(3, 3, figsize=(15, 12))

# --- Pol-noll ---
for i, (sys, title) in enumerate(zip(systems, titles)):
    p = sys.poles
    z = sys.zeros
    axes[0, i].scatter(np.real(z), np.imag(z), marker='o', facecolors='none', edgecolors='b', s=100, label='Nollor')
    axes[0, i].scatter(np.real(p), np.imag(p), marker='x', color='r', s=100, label='Poler')
    axes[0, i].set_title(f"Pol–noll karta för {title}")
    axes[0, i].set_xlabel("Re(s)")
    axes[0, i].set_ylabel("Im(s)")
    axes[0, i].grid(True)
    axes[0, i].legend()
# --- Impulssvar ---
for i, (sys, title) in enumerate(zip(systems, titles)):
    t, y = signal.impulse(sys)
    axes[1, i].plot(t, y)
    axes[1, i].grid(True)
    axes[1, i].set_title(f"Impulssvar för {title}")
    axes[1, i].set_xlabel("Tid [s]")
    axes[1, i].set_ylabel("Amplitude")

# --- Bode ---
for i, (sys, title) in enumerate(zip(systems, titles)):
    w, mag, phase = signal.bode(sys)

    ax_mag = axes[2, i]
    ax_phase = ax_mag.twinx()

    ax_mag.semilogx(w, mag, 'b')
    ax_mag.set_ylabel("Magnitude [dB]", color='b')
    ax_mag.set_xlabel("Frekvens [rad/s]")
    ax_mag.grid(True, which="both")

    ax_phase.semilogx(w, phase, 'r--')
    ax_phase.set_ylabel("Fas [°]", color='r')

    ax_mag.set_title(f"Bode-diagram för {title}")

plt.tight_layout()
plt.show()