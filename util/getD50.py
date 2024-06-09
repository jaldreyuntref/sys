import numpy as np

def getD50(signal, fs):
    t50 = int(0.05 * fs)
    signalSquared = signal ** 2
    energyBefore50ms = np.sum(signalSquared[0:t50]) / fs
    energyAfter50ms = np.sum(signalSquared[t50:]) / fs
    return (energyBefore50ms / energyAfter50ms) * 100