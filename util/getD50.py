import numpy as np

def getD50(signal, fs):
    t50 = int(0.05 * fs)
    signalSquared = signal ** 2
    energyBefore50ms = np.sum(signalSquared[0:t50]) / fs
    totalEnergy = np.sum(signalSquared) / fs
    return (energyBefore50ms / totalEnergy) * 100