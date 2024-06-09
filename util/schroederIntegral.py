import numpy as np

def schroederIntegral(signal):
    p = np.flip(signal)**2
    schroeder_integral = np.cumsum(p)[::-1]
    schroeder_integral /= np.max(np.abs(schroeder_integral)) 
    schroeder_integral = np.array(schroeder_integral)
    return schroeder_integral

"""
t = np.linspace(0, 10, fs*10)
signal = np.sin(np.pi*t)

schroederIntegralSignal = schroederIntegral(signal)


plot(t, schroederIntegralSignal)
"""