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
    from functions import getWAVData, createFigure
    
    ir, time, fs = getWAVData("entregas_parciales\segunda_entrega\media\synthesized-impulse-response.wav")
    ir_log = logarithmicScaleConversion(ir)

    fig, ax = createFigure(time, ir_log)
    ax.set_ylim([-70, 0])
    plt.show()