import numpy as np

def calculateFourierCoefficients(wave, t, N=20, T=1):
    a0 = 2 * np.mean(wave)
    an = np.zeros(N)
    bn = np.zeros(N)
    for n in range(1, N + 1):
        an[n-1] = 2 * np.mean(wave * np.cos(2 * np.pi * n * t / T))
        bn[n-1] = 2 * np.mean(wave * np.sin(2 * np.pi * n * t / T))
    return a0, an, bn


def reconstructWave(a0, an, bn, t, N=10, T=1):
    reconstructedWave = a0 / 2 * np.ones_like(t)
    for n in range(1, N + 1):
        reconstructedWave += an[n-1] * np.cos(2 * np.pi * n * t / T) + bn[n-1] * np.sin(2 * np.pi * n * t / T)
    return reconstructedWave
