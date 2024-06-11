from scipy.signal import hilbert
import numpy as np

def hilbertTransform(signal):

    """
    Applies the Hilbert transform to a signal to obtain its envelope.

    Parameters:
        signal (numpy array): The input signal.

    Returns:
        numpy array: The normalized envelope of the input signal.

    This function computes the analytic signal of the input using the Hilbert 
    transform and extracts its envelope. The envelope is then normalized by 
    dividing by the maximum absolute value of the envelope.
    """

    analytic_signal = hilbert(signal)
    envelope = np.abs(analytic_signal)
    return envelope / np.max(np.abs(envelope))


if __name__ == "__main__":
    from synthesizeImpulseResponse import synthesizeImpulseResponse
    from functions import plot

    impulseResponse,time = synthesizeImpulseResponse(test=True)
    plot(time, hilbertTransform(impulseResponse), title="hilbertTransform result")
