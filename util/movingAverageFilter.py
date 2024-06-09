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
    
    return y

"""
t = np.linspace(0, 10, fs*10)
signal = 5*np.sin(2*np.pi*t) + np.sin(10 * 2*np.pi*t) + np.sin(16000 * 2*np.pi*t)

plot(t, signal)

filteredSignal = movingAverageFilter(signal, 22000)
time = np.linspace(0, len(signal) / fs, len(signal))

plot(time, filteredSignal)

filteredSignal
"""
