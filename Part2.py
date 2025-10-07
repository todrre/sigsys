# Del 2
# 1) samplingsfrekvensen måste vara över 2 * 8kHz enligt Nyquist teoremet
# Men högst 24kHz
# Så den kan vara exempelvis 18kHz 

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import control as ct

# 2) 
# Spec för A-A filter:
fs = int(18e3) # Samplingsfrekvens
fp = 8e3 # Passbandfrekvens
fb = 9e3 # Stoppbandfrekvens
mr = 3 # Max rippel
md = np.abs(20*np.log10(2**-12)) # Min dämpning
t = np.linspace(0, 1, fs)

# 3)
N, Wn = signal.cheb1ord(wp=2*np.pi * fp, ws=2 * np.pi * fb, gpass=mr, gstop=md, analog=True)
print(N)
b, a = signal.cheby1(N, mr, Wn, 'low', analog=True)
LP_filter = signal.lti(b,a)

# Beräkna Bode-svaret
w, mag, phase = signal.bode(LP_filter)

# Skapa figuren
fig, ax1 = plt.subplots(figsize=(10, 6))
fig.suptitle(f'Bode-diagram för Chebyshev Typ I Filter (N={int(N)})', fontsize=14)

# --- Amplitudplot (Vänster y-axel) ---
# Konvertera W (rad/s) till frekvens i Hz
freq_hz = w / (2 * np.pi) 

ax1.semilogx(freq_hz, mag, color='tab:blue', linewidth=2)
ax1.set_xlabel('Frekvens (Hz)')
ax1.set_ylabel('Amplitud (dB)', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.grid(True, which="both", linestyle='--')

# Lägg till specifikationslinjer
ax1.axvline(fp, color='green', linestyle='--', label=f'fp ({fp/1e3:.0f} kHz)')
ax1.axvline(fb, color='orange', linestyle='--', label=f'fb ({fb/1e3:.0f} kHz)')
ax1.axhline(-mr, color='green', linestyle=':')
ax1.axhline(-md, color='orange', linestyle=':')
ax1.legend(loc='upper right')

# --- Fasplot (Höger y-axel) ---
ax2 = ax1.twinx()  # Skapar en delad x-axel men egen y-axel
ax2.semilogx(freq_hz, phase, color='tab:red', linewidth=2, linestyle='-')
ax2.set_ylabel('Fas (grader)', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

plt.show()

# 4)
signal_och_brus = np.sin(2 * np.pi * 7e3 * t) + np.sin(2 * np.pi * 11e3 * t)


T_out, y_out = ct.forced_response(LP_filter, T=t, U=signal_och_brus)

