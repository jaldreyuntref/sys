import numpy as np

def getC80(signal, fs):
    """
    Calculates the clarity index (C80) of a given audio signal.

    Parameters:
        signal (numpy array): The input audio signal.
        fs (int): The sampling rate in Hz.

    Returns:
        float: The C80 clarity index in decibels (dB).

    This function computes the C80 index, which is a measure of the clarity of 
    an audio signal. It calculates the ratio of the early to late energy, 
    where the early energy is the energy within the first 80 milliseconds 
    and the late energy is the energy after 80 milliseconds. The result is 
    expressed in decibels (dB).
    """
        
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
