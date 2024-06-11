import numpy as np

def getD50(signal, fs):
    """
    Calculates the definition index (D50) of a given audio signal.

    Parameters:
        signal (numpy array): The input audio signal.
        fs (int): The sampling rate in Hz.

    Returns:
        float: The D50 definition index as a percentage.

    This function computes the D50 index, which is a measure of the speech 
    intelligibility of an audio signal. It calculates the ratio of the 
    early energy (within the first 50 milliseconds) to the total energy 
    of the signal. The result is expressed as a percentage.
    """
        
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