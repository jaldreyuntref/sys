import numpy as np
import soundfile as sf

def generateSineSweepInverseFilter(finf, fsup, t0, fs):

    """
    Generates a sine sweep signal and its inverse filter.

    Parameters:
        finf (float): The initial frequency of the sweep in Hz.
        fsup (float): The final frequency of the sweep in Hz.
        t0 (float): The duration of the sweep in seconds.
        fs (int): The sampling rate in Hz.

    Returns:
        tuple: A tuple containing the sine sweep signal (numpy array), 
               the inverse filter signal (numpy array), and the time vector (numpy array).

    This function generates a sine sweep from finf to fsup over a period of t0 seconds 
    and calculates its inverse filter. Both the sine sweep and the inverse filter 
    are saved as WAV files in the 'entrega_final/obtain-IR/' directory.
    """

    wi = 2*np.pi*finf
    ws = 2*np.pi*fsup

    R = np.log(ws/wi)
    K = (t0*wi)/R
    L = t0/R
    t = np.linspace(0,t0,t0*fs)

    sine_sweep = np.sin(K*(np.exp(t/L)-1))
    sine_sweep = sine_sweep * 0.5

    m = wi/(2*np.pi*(K/L)*np.exp(t/L)) 

    filtro_inverso = m*sine_sweep[::-1]
    filtro_inverso = filtro_inverso * 5

    sf.write("entrega_final/obtain-IR/sine-sweep.wav", sine_sweep, samplerate=fs)
    sf.write("entrega_final/obtain-IR/inverse-filter.wav", filtro_inverso, samplerate=fs)

    return (sine_sweep, filtro_inverso, t)

if __name__ == "__main__":
    generateSineSweepInverseFilter(20, 2000, 5, 44100)
    print("Sine sweep and inverse filter generated in obtain-IR.")