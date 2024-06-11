import numpy as np

def getC80(signal, fs):
    t80 = int(0.08 * fs)
    signalSquared = signal ** 2
    energyBefore80ms = np.sum(signalSquared[:t80]) / fs
    energyAfter80ms = np.sum(signalSquared[t80:]) / fs
    return 10 * np.log10(energyBefore80ms / energyAfter80ms)


if __name__ == "__main__":
    from synthesizeImpulseResponse import synthesizeImpulseResponse
    from hilbertTransform import hilbertTransform
    from movingAverageFilter import movingAverageFilter

    impuseResponse, time = synthesizeImpulseResponse(test=True)
    smoothedImpulseResponse = movingAverageFilter(hilbertTransform(impuseResponse), 2200)

    print("C80: ", getC80(impuseResponse, 44100))
