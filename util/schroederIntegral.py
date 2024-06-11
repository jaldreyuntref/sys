import numpy as np

def schroederIntegral(signal):
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

