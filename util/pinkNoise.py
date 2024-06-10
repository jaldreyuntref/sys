import numpy as np
import pandas as pd
from scipy.io import wavfile

def pinkNoise(t, fs=44100):

    """
    
    Esta función implementa la versión 2 del método de Voss para generar ruido rosa,
    el cual se caracteriza por tener la misma densidad espectral de potencia por 
    cada octava de frecuencia.

    ¿Cómo lo hace?
        * Transforma todas más muestras obtenidas a partir de multiplicar la frecuencia de
            muestreo (fs) por los segundos en columnas de una matriz.
        * Otorga valores aleatorios a cada una de esas muestras y las asigna a una fila de
            dicha matriz.
        * Genera la matriz a partir de dicha información.
        * Genera un archivo WAV a partir de la matriz, que contiene el ruido rosa generado, 
            normalizado.

    Parámetros:
        t (float): Duración del ruido rosa en segundos.
        fs (int, opcional): Frecuencia de muestreo del ruido rosa (Hz). 
            Por defecto es 44100 Hz.

    Retorno:
        ndarray: Arreglo de NumPy que representa el ruido rosa generado.

    """
    
    nrows = fs * t
    ncols = 16
    array = np.full((nrows, ncols), np.nan)
    array[0, :] = np.random.random(ncols)
    array[:, 0] = np.random.random(nrows)
    
    # el numero total de cambios es nrows
    n = nrows
    cols = np.random.geometric(0.5, n)
    cols[cols >= ncols] = 0
    rows = np.random.randint(nrows, size=n)
    array[rows, cols] = np.random.random(n)
    
    df = pd.DataFrame(array)
    filled = df.fillna(method='ffill', axis=0)
    total = filled.sum(axis=1)
    
    ## Centrado de el array en 0
    total = total - total.mean()
    
    ## Normalizado
    valor_max = max(abs(max(total)),abs(min(total)))
    total = total / valor_max
    
    # Agregar generación de archivo de audio .wav
    wavfile.write("media/ruidoRosa.wav", fs, np.int16(total * 32767))

    return total