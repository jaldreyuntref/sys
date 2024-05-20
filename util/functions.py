import matplotlib.pyplot as plt
import wave
import numpy as np
import pandas as pd

def plot(xVector, yVector, xLabel = "Times (s)", yLabel = "Amplitude", title = "Signal", scale=None):
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
            bit_depth = sampwidth * 8
            if bit_depth != 16:
                print("Please enter a signal with a bit depth resolution of 16!") 
                return
            signal = np.frombuffer(audioData, dtype=np.int16)
            nChannels = wf.getnchannels()
            signal = signal[0::2] if nChannels == 2 else signal
            time = np.linspace(0, duration, num=nSamples)

            return signal, time

def plotWAV(route, xLabel, yLabel, title, scale=None):
    signal, time = getWAVData(route)
    plot(time, signal, xLabel, yLabel, title, scale)

    
def getDataFrameData(route):
    dataFrame = pd.read_csv(route, sep='\t', skiprows=1, header=None)
    return dataFrame.iloc[:, 0], dataFrame.iloc[:, 1]

def plotDataFrame(route, xLabel, yLabel, title, scale=None):
    y, x = getDataFrameData(route)
    plot(y, x, xLabel, yLabel, title, scale)


