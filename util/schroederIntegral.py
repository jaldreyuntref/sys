import numpy as np

def schroederIntegral(signal):

    """
    Computes the Schroeder integral of a given signal.

    Parameters:
        signal (numpy array): The input signal.

    Returns:
        numpy array: The Schroeder integral of the input signal, normalized by its maximum absolute value.

    This function calculates the Schroeder integral, which is the cumulative sum of the squared 
    reversed signal values. The result is then normalized by dividing by the maximum absolute 
    value of the Schroeder integral.
    """

    p = np.flip(signal)**2
    schroeder_integral = np.cumsum(p)[::-1]
    schroeder_integral /= np.max(np.abs(schroeder_integral)) 
    schroeder_integral = np.array(schroeder_integral)
    return schroeder_integral


if __name__ == "__main__":
    from synthesizeImpulseResponse import synthesizeImpulseResponse
    from functions import plot

    impulseResponse,time = synthesizeImpulseResponse(test=True)
    plot(time, schroederIntegral(impulseResponse), title="schroederIntegral result")

