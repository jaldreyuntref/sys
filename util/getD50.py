import numpy as np

def getD50(signal, fs):
    t50 = int(0.05 * fs)
    signalSquared = signal ** 2
    energyBefore50ms = np.sum(signalSquared[0:t50]) / fs
    totalEnergy = np.sum(signalSquared) / fs
    return (energyBefore50ms / totalEnergy) * 100

if __name__ == "__main__":
    from synthesizeImpulseResponse import synthesizeImpulseResponse
    from hilbertTransform import hilbertTransform
    from movingAverageFilter import movingAverageFilter

    impuseResponse, time = synthesizeImpulseResponse(test=True)
    smoothedImpulseResponse = movingAverageFilter(hilbertTransform(impuseResponse), 2200)

    print("D50: ", getD50(impuseResponse, 44100))