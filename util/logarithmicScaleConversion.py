import numpy as np

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