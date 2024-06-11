import numpy as np
import matplotlib.pyplot as plt

def logarithmicScaleConversion(signal):
    """

    Converts a signals vertical axis into logarithmic scale.

    Parameters:
        signal (list): The signal to be converted.

    Returns:
        list: The converted signal.

    """
    signal = np.where(signal == 0, 1e-10, signal)
    return 20 * np.log10(np.abs(signal/np.max(signal)))


if __name__ == "__main__":
    from functions import createFigure
    from synthesizeImpulseResponse import synthesizeImpulseResponse
    
    impulseResponse, time = synthesizeImpulseResponse(test=True)
    impulseResponseLog = logarithmicScaleConversion(impulseResponse)

    fig, ax = createFigure(time, impulseResponseLog)
    ax.set_ylim([-70, 0])
    plt.show()