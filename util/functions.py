import matplotlib.pyplot as plt
import wave
import numpy as np
import pandas as pd
from scipy.io import wavfile
import soundfile as sf
import yaml

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

def plotWAV(route, xLabel, yLabel, title, scale=None):
    signal, time = getWAVData(route)
    plot(time, signal, xLabel, yLabel, title, scale)

def getDataFrameData(route):
    dataFrame = pd.read_csv(route, sep='\t', skiprows=1, header=None)
    return dataFrame.iloc[:, 0], dataFrame.iloc[:, 1]

def plotDataFrame(route, xLabel, yLabel, title, scale="log"):
    x, y = getDataFrameData(route)
    plot(x, y, xLabel, yLabel, title, scale)

def getWAVData(route, channel=0):
    WAV = wavfile.read(route)
    signal = WAV[1]
    if len(signal.shape) > 1:  
        signal = signal[:, channel]
    time = np.linspace(0, len(signal) / WAV[0], len(signal))
    signal = signal / np.max(np.abs(signal))
    return signal, time, WAV[0]
