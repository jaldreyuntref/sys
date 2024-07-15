import numpy as np

def sawtooth(frequency=1, samplingRate=44100, duration=5):
    t = np.linspace(0, duration, int(samplingRate * duration))
    sawtoothWave = 2 * (t * frequency - np.floor(0.5 + t * frequency))

    return sawtoothWave, t
