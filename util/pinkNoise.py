import numpy as np
import pandas as pd
from scipy.io import wavfile

def pinkNoise(t, fs=44100):

    """
    Generates pink noise using Voss's method (version 2), which is characterized by 
    having the same power spectral density per octave of frequency.

    Parameters:
        t (float): Duration of the pink noise in seconds.
        fs (int, optional): Sampling frequency of the pink noise in Hz. 
                            Default is 44100 Hz.

    Returns:
        numpy.ndarray: A NumPy array representing the generated pink noise.
    """
    
    nrows = fs * t
    ncols = 16
    array = np.full((nrows, ncols), np.nan)
    array[0, :] = np.random.random(ncols)
    array[:, 0] = np.random.random(nrows)
    
    n = nrows
    cols = np.random.geometric(0.5, n)
    cols[cols >= ncols] = 0
    rows = np.random.randint(nrows, size=n)
    array[rows, cols] = np.random.random(n)
    
    df = pd.DataFrame(array)
    filled = df.fillna(method='ffill', axis=0)
    total = filled.sum(axis=1)
    
    total = total - total.mean()

    valor_max = max(abs(max(total)),abs(min(total)))
    total = total / valor_max
    
    wavfile.write("entrega_final/obtain-IR/pink-noise.wav", fs, np.int16(total * 32767))

    return total

if __name__ == "__main__":
    pinkNoise(5, 44100)
    print("Pink noise generated in obtain-IR/pink-noise.wav")