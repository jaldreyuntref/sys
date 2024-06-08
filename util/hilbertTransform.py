from scipy.signal import hilbert
import numpy as np

def hilbertTransform(signal):
    analytic_signal = hilbert(signal)
    envelope = np.abs(analytic_signal)
    return envelope


if __name__ == "__main__":
    t = np.linspace(0, 10, 44100*10)
    signal = np.sin(2*np.pi*t) + np.sin(10 * 2*np.pi*t) + np.sin(16000 * 2*np.pi*t)

    hilbertTransformSignal = hilbertTransform(signal)

    #plot(t, signal)
    #plot(t, hilbertTransformSignal)
