import matplotlib.pyplot as plt
import wave
import numpy as np

def plot(xVector, yVector, xLabel, yLabel, title, scale=None):
    plt.plot(xVector, yVector)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.xscale(scale) if scale is not None else None
    plt.title(title)
    plt.grid(True)
    plt.show()

def askBooleanInput(prompt):
    user_input = input(prompt + " (yes/no): ").strip().lower()
    if user_input in ['yes', 'y']:
        return True
    elif user_input in ['no', 'n']:
        return False
    else:
        return askBooleanInput("Invalid input. Please enter 'yes' or 'no'.")

def plotWAV(route, xLabel, yLabel, title, scale=None): #preguntar que hacer con el bit depth
    with wave.open(route, 'rb') as wf:
        fs = wf.getframerate()
        nSamples = wf.getnframes()
        duration = nSamples / fs
        audioData = wf.readframes(nSamples)
        #sampwidth = wf.getsampwidth()
        #bit_depth = sampwidth * 8
        #print("depth", bit_depth)
        signal = np.frombuffer(audioData, dtype=np.int16)
        nChannels = wf.getnchannels()
        signal = signal[0::2] if nChannels == 2 else signal
        time = np.linspace(0, duration, num=nSamples)

        plot(time, signal, xLabel, yLabel, title, scale) # Plots only one channel (se podria hacer para que se pase en stereo o no)