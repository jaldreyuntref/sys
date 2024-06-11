from scipy.signal import hilbert
import numpy as np

def hilbertTransform(signal):
    analytic_signal = hilbert(signal)
    envelope = np.abs(analytic_signal)
    return envelope / np.max(np.abs(envelope))


if __name__ == "__main__":
    from synthesizeImpulseResponse import synthesizeImpulseResponse
    from functions import plot

    impulseResponse,time = synthesizeImpulseResponse(test=True)
    plot(time, hilbertTransform(impulseResponse), title="hilbertTransform result")
