import numpy as np

def getC80(signal, fs):
    t80 = int(0.08 * fs)
    signalSquared = signal ** 2
    energyBefore80ms = np.sum(signalSquared[:t80]) / fs
    energyAfter80ms = np.sum(signalSquared[t80:]) / fs
    return 10 * np.log10(energyBefore80ms / energyAfter80ms)

