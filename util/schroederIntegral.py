import numpy as np

def schroederIntegral(signal):
    absoluteSignal = np.abs(signal) / np.max(np.abs(signal))
    schroederIntegral = np.cumsum(absoluteSignal[::-1]**2)[::-1]
    return schroederIntegral/np.max(np.abs(schroederIntegral)) 

"""
t = np.linspace(0, 10, fs*10)
signal = np.sin(np.pi*t)

schroederIntegralSignal = schroederIntegral(signal)


plot(t, schroederIntegralSignal)
"""