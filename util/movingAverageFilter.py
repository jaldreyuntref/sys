import numpy as np

def movingAverageFilter(signal, L):
    y = np.zeros_like(signal)
    cumsum = np.cumsum(signal)
    y[:L] = cumsum[:L] / np.arange(1, L + 1)
    y[L:] = (cumsum[L:] - cumsum[:-L]) / L
    return y

"""
t = np.linspace(0, 10, fs*10)
signal = 5*np.sin(2*np.pi*t) + np.sin(10 * 2*np.pi*t) + np.sin(16000 * 2*np.pi*t)

plot(t, signal)

filteredSignal = movingAverageFilter(signal, 22000)
time = np.linspace(0, len(signal) / fs, len(signal))

plot(time, filteredSignal)

filteredSignal
"""
