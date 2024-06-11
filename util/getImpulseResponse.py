from scipy.signal import fftconvolve
import numpy as np

def getImpulseResponse(sineSweep, inverseFilter):

    """
    Obtains the impulse response through the convolution of a sine sweep and its inverse filter, with the method proposed by Angelo Farina.

    Parameters:
        sineSweep (list): The sine sweep.
        inverseFilter (list): The inverse filter of the sine sweep.

    Returns:
        list: The impulse response.

    """ 

    impulseResponse = fftconvolve(sineSweep, inverseFilter)
    halfIndex = len(impulseResponse) // 2
    impulseResponse = impulseResponse[halfIndex:]
    impulseResponse = impulseResponse / np.max(np.abs(impulseResponse))

    return impulseResponse

if __name__ == "__main__":
    from generateSineSweepInverseFilter import generateSineSweepInverseFilter
    from functions import createFigure
    import matplotlib.pyplot as plt

    sineSweep, inverseFilter, time = generateSineSweepInverseFilter(20, 4000, 5, 44100)
    impulseResponse = getImpulseResponse(sineSweep, inverseFilter)
    fig, ax = createFigure(time, impulseResponse , "Time (s)", "Amplitude", "Impulse Response")
    ax.set_xlim([-0.01, 0.01])
    plt.show()