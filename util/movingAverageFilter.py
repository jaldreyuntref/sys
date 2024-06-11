import numpy as np

def movingAverageFilter(signal, L):

    """
    Applies a moving average filter to a signal.

    Parameters:
        signal (numpy array): The input signal to be filtered.
        L (int): The window length of the moving average filter.

    Returns:
        numpy array: The filtered signal, normalized by the maximum absolute value.

    This function computes a moving average of the input signal with a specified 
    window length `L`. It iteratively calculates the average of the signal within 
    the window and adjusts for new incoming samples. The resulting filtered signal 
    is then normalized by dividing by its maximum absolute value.
    """
    
    y = np.zeros(len(signal))
    previousTotal = 0
    for sampleNumber in range(len(signal)):
        if(sampleNumber) <= (L - 1):
            total = (previousTotal + signal[sampleNumber]) 
            previousTotal = total
            average = total / (sampleNumber + 1)
        else:
            total = previousTotal + signal[sampleNumber] - signal[sampleNumber - L]
            average = total / L
            previousTotal = total
        y[sampleNumber] = average
    
    return y / np.max(np.abs(y))

if __name__ == "__main__":
    from synthesizeImpulseResponse import synthesizeImpulseResponse
    from functions import plot

    impulseResponse,time = synthesizeImpulseResponse(test=True)
    plot(time, movingAverageFilter(impulseResponse, 200), title="movingAverageFilter result")
