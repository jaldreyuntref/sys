import numpy as np

def movingAverageFilter(signal, L):
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
