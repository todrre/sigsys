# Uppgift 7

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal


# 1. Grundparametrar
f_0 = 100         # grundfrekvens [Hz]
T_0 = 1 / f_0     # period [s]
fs = 10000    # samplingsfrekvens [Hz]
t = np.arange(0, 20*T_0, 1/fs)   # simulera 5 perioder
h = 1             # amplitud


a = 500 #1930 # Denna behöver räknas ut och är idag en gissning
b = 0.32 # Denna är uträknad 1 / (2 * c * np.sqrt(1 - c ** 2)), b = 2c
H_1 = signal.lti([a**2], [1, b * a, a ** 2]) # I nuläget är det ett inverterande lp-filter

# 2. Definiera Fourierserie för triangulär våg
def triangel_term(n, t, L):
    return 1 / (2 * n - 1) ** 2 * np.cos((2 * n - 1) * np.pi * t / L)

def triangelvåg(t, h, L, N=9):
    # N = antal termer i Fourierserien (ju fler, desto mer "ideal")
    return h / 2 + 4 * h / np.pi ** 2 * sum(triangel_term(n, t, L) for n in range(1, N+1))

# 3. Skapa signal
u = triangelvåg(t, h, T_0, N=9)

tout, yout, xout = signal.lsim(H_1, U=u, T=t)

# 5. Plotta resultatet
plt.figure(figsize=(10, 4))
plt.plot(t, u, label="Ingång (triangulär våg)", alpha=0.7)
plt.plot(tout, yout, label="Utgång (efter LP-filter)", linewidth=2)
plt.xlabel("Tid [s]")
plt.ylabel("Amplitud")
plt.title("Systemrespons med forced_response()")
plt.legend()
plt.grid(True)
plt.show()