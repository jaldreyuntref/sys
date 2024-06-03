import matplotlib.pyplot as plt
import wave
import numpy as np
import pandas as pd
from scipy.io import wavfile
import soundfile as sf
from scipy.signal import fftconvolve

def plot(xVector, yVector, xLabel = "Time (s)", yLabel = "Amplitude", title = "Signal", scale=None):
    plt.plot(xVector, yVector)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.xscale(scale) if scale is not None else None
    plt.title(title)
    plt.grid(True)
    plt.show()

def createFigure(xVector, yVector, xLabel = "Times (s)", yLabel = "Amplitude", title = "Signal", scale=None):
    fig, ax = plt.subplots()
    ax.plot(xVector, yVector)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.set_title(title)
    ax.set_xscale(scale) if scale is not None else None
    ax.grid(True)
    return fig, ax

def askBooleanInput(prompt):
    user_input = input(prompt + " (yes/no): ").strip().lower()
    if user_input in ['yes', 'y']:
        return True
    elif user_input in ['no', 'n']:
        return False
    else:
        return askBooleanInput("Invalid input. Please enter 'yes' or 'no'.")
    
def getWAVData(route):
        with wave.open(route, 'rb') as wf:
            fs = wf.getframerate()
            nSamples = wf.getnframes()
            duration = nSamples / fs
            audioData = wf.readframes(nSamples)
            sampwidth = wf.getsampwidth()
            bitDepth = sampwidth * 8
            if bitDepth != 16:
                signal, time = getWAVDataNon16Bit(route)
                return signal, time
            signal = np.frombuffer(audioData, dtype=np.int16)
            nChannels = wf.getnchannels()
            signal = signal[0::2] if nChannels == 2 else signal
            signal = signal / np.max(np.abs(signal))
            time = np.linspace(0, duration, num=nSamples)

            return signal, time

def plotWAV(route, xLabel, yLabel, title, scale=None):
    signal, time = getWAVData(route)
    plot(time, signal, xLabel, yLabel, title, scale)

    
def getDataFrameData(route):
    dataFrame = pd.read_csv(route, sep='\t', skiprows=1, header=None)
    return dataFrame.iloc[:, 0], dataFrame.iloc[:, 1]

def plotDataFrame(route, xLabel, yLabel, title, scale="log"):
    x, y = getDataFrameData(route)
    plot(x, y, xLabel, yLabel, title, scale)

def getWAVDataNon16Bit(route):
    WAV = wavfile.read(route)
    signal = WAV[1]
    time = np.linspace(0, len(signal) / WAV[0], len(signal))
    signal = signal / np.max(np.abs(signal))
    return signal, time


def generarSineSweepYFiltroInverso(finf, fsup, t0):

    wi = 2*np.pi*finf
    ws = 2*np.pi*fsup

    R = np.log(ws/wi)
    K = (t0*wi)/R
    L = t0/R
    fs = 44100
    t = np.linspace(0,t0,t0*fs)

    # Definición del sine sweep
    sine_sweep = np.sin(K*(np.exp(t/L)-1))
    sine_sweep = sine_sweep * 0.5 # para equiparar las amplitudes del sine sweep y el filtro inverso

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.plot(t, sine_sweep)
    ax1.set_ylabel('Amplitud')
    ax1.set_title('Sine Sweep')
    ax1.grid(True)

    # Definición de la modulacion
    m = wi/(2*np.pi*(K/L)*np.exp(t/L))  # (K/L)*math.exp(t/L) = w(t) en la consigna

    # Definición del filtro inverso
    filtro_inverso = m*sine_sweep[::-1]
    filtro_inverso = filtro_inverso * 5 # para equiparar las amplitudes del sine sweep y el filtro inverso

    ax2.plot(t, filtro_inverso)
    ax2.set_ylabel('Amplitud')
    ax2.set_title('Filtro Inverso')
    ax2.grid(True)

    plt.xlabel('Tiempo (s)')
    fig.suptitle('Sine Sweep y Filtro Inverso - Dominio Temporal')

    wavfile.write("media/sine-sweep.wav", fs, np.int16(sine_sweep * 32767))
    wavfile.write("media/filtro-inverso.wav", fs, np.int16(filtro_inverso * 32767))

    return (sine_sweep, filtro_inverso, t)

def getImpulseResponse(sineSweep, inverseFilter):
    impulseResponse = fftconvolve(sineSweep, inverseFilter)
    halfIndex = len(impulseResponse) // 2
    impulseResponse = impulseResponse[halfIndex:]
    impulseResponse = impulseResponse / np.max(np.abs(impulseResponse))

    return impulseResponse


