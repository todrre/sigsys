# Del 2
# 1) samplingsfrekvensen måste vara över 2 * 8kHz enligt Nyquist teoremet
# Men högst 24kHz
# Så den kan vara exempelvis 18kHz 

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

# 2) 
# Spec för A-A filter:
fs = 16e3 # Samplingsfrekvens (rad/s) Eftersom det är ett analogt så sker filtreringen innan samplingen 
fp = 8e3  # Passbandfrekvens (rad/s)
fb = 11e3 # Stoppbandfrekvens (rad/s)
mr = 3 # Max rippel (dB)
md = np.abs(20*np.log10(2**-12)) # Min dämpning (dB)

wp = fp * 2 * np.pi
wb = fb * 2 * np.pi

# 3)
N, Wn = signal.cheb1ord(wp=wp, ws=wb, gpass=mr, gstop=md, analog=True)
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

t = np.linspace(0, 0.1, int(fs))
u = np.sin(2 * np.pi * 7e3 * t) + np.sin(2 * np.pi * 15e3 * t)

tout, yout, xout = signal.lsim(LP_filter, U=u, T=t)

plt.plot(t, u, 'r', alpha=0.5, linewidth=1, label='input')
plt.plot(tout, yout, 'k', linewidth=1.5, label='output')
plt.legend(loc='best', shadow=True, framealpha=1)
plt.grid(alpha=0.3)
plt.xlabel('t')
plt.show()

# --- FFT-del ---
N = len(t)
yout_fft = np.fft.fft(yout, N)

T = 1 / fs
freq = np.linspace(0, fs, N//100, endpoint=False)/1000

# Ta endast den positiva halvan
half_N = N // 2
yout_magnitude = np.abs(yout_fft) / np.max(np.abs(freq))

# Subsampla var 100:e punkt för plot
step = 100
freq_plot = freq  # till kHz
yout_magnitude_plot = yout_magnitude[::step]

# --- Plotta spektrum ---
plt.figure(figsize=(10, 5))
# plt.stem(freq_plot, u_magnitude_plot, linefmt='r-', markerfmt='ro', basefmt=' ', label='Input Spektrum (u)')
plt.stem(freq_plot, yout_magnitude_plot, linefmt='k-', markerfmt='ko', basefmt=' ', label='Output Spektrum (yout)')

plt.legend(loc='best', shadow=True, framealpha=1)
plt.grid(alpha=0.3)
plt.xlabel('Frekvens (kHz)')
plt.ylabel('Magnitud')
plt.title('Magnitudspektrum i frekvensdomän')
plt.xlim(0, fs/2 * 1e-3)  # bara positiva frekvenser upp till Nyquist
plt.ylim(bottom=0)
plt.show()
