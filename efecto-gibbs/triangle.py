import numpy as np

def triangle(frequency=1, samplingRate=44100, duration=5):
    t = np.linspace(0, duration, int(samplingRate * duration))
    triangleWave = 2 * np.abs(2 * (t * frequency - np.floor(0.5 + t * frequency))) - 1

    return triangleWave, t
