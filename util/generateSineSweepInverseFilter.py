import numpy as np
import soundfile as sf

def generateSineSweepInverseFilter(finf, fsup, t0, fs):

    """
    Genera un sine sweep (barrido sinusoidal) y su filtro inverso.

    Esta función genera un barrido sinusoidal que incrementa su frecuencia 
    desde una frecuencia inicial (`finf`) hasta una frecuencia final (`fsup`) 
    en un tiempo determinado (`t0`). También calcula su filtro inverso.

    Parámetros:
        finf, fsuy y t0, siendo los tres float que representan la frecuencia inicial,
        final (expresadas en Hz) y la duración (en segundos) del barrido respectivamente.

    Retorno:
        Una tupla que contiene: sine_sweep, filtro_inverso y t, siendo los tres arreglos
        de numpy que representan el barrido sinusoidal, el filtro inverso y el eje temporal
        respectivamente.

    """

    wi = 2*np.pi*finf
    ws = 2*np.pi*fsup

    R = np.log(ws/wi)
    K = (t0*wi)/R
    L = t0/R
    t = np.linspace(0,t0,t0*fs)

    # Definición del sine sweep
    sine_sweep = np.sin(K*(np.exp(t/L)-1))
    sine_sweep = sine_sweep * 0.5 # para equiparar las amplitudes del sine sweep y el filtro inverso

    # Definición de la modulacion
    m = wi/(2*np.pi*(K/L)*np.exp(t/L))  # (K/L)*math.exp(t/L) = w(t) en la consigna

    # Definición del filtro inverso
    filtro_inverso = m*sine_sweep[::-1]
    filtro_inverso = filtro_inverso * 5 # para equiparar las amplitudes del sine sweep y el filtro inverso


    sf.write("entrega_final/obtain-IR/sine-sweep.wav", sine_sweep, samplerate=fs)
    sf.write("entrega_final/obtain-IR/inverse-filter.wav", filtro_inverso, samplerate=fs)

    return (sine_sweep, filtro_inverso, t)

if __name__ == "__main__":
    generateSineSweepInverseFilter(20, 2000, 5, 44100)
    print("Sine sweep and inverse filter generated in obtain-IR.")