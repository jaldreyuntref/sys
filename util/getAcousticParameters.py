import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('')
import os
print(os.getcwd())

fs = 48000

from util.linearRegression import linearRegression

def getAcousticParameters(signal):

    signalAbove5db = None
    signalBetween5dbAnd35db = None
    signalBetween5dbAnd25db = None
    signalBetween5dbAnd15db = None
    edt = None
    time = np.linspace(0, len(signal) / fs, len(signal))

    for i in range(len(signal) - 10000):
        if signal[i] <= -5 and signalAbove5db is None:
            if np.all(signal[i:i + 10000] <= -5):
                signalAbove5db = signal[i:]
                time5db = time[i]

        if signal[i] <= -10 and edt is None:
            if np.all(signal[i:i + 10000] <= -10):
                edt = time[i]

        if signal[i] <= -15 and signalBetween5dbAnd15db is None:
            if np.all(signal[i:i + 10000] <= -15):
                signalBetween5dbAnd15db = signalAbove5db[:i]
                time15db = time[i]
        
        if signal[i] <= -25 and signalBetween5dbAnd25db is None:
            if np.all(signal[i:i + 10000] <= -25):
                signalBetween5dbAnd25db = signalAbove5db[:i]
                time25db = time[i]

        if signal[i] <= -35 and signalBetween5dbAnd35db is None:
            if np.all(signal[i:i + 10000] <= -35):
                signalBetween5dbAnd35db = signalAbove5db[:i]
                time35db = time[i]
                break
    
    if signalAbove5db is None:
        print("Error, the signal doesnt fall beneath 5db for an extender period of time, please check the integrity of the signal")
        # handle the error

    if signalBetween5dbAnd35db is None:
        print("Error, the signal doesnt fall beneath 35db for an extender period of time, please check the integrity of the signal")
        # handle the error

    if signalBetween5dbAnd25db is None:
        print("Error, the signal doesnt fall beneath 25db for an extender period of time, please check the integrity of the signal")
        # handle the error

    if signalBetween5dbAnd15db is None:
        print("Error, the signal doesnt fall beneath 15db for an extender period of time, please check the integrity of the signal")
        # handle the error

    m15, b15 = linearRegression(signalBetween5dbAnd15db)
    t60Fromt10 = ((-60 - b15) / m15) / fs
    m25, b25 = linearRegression(signalBetween5dbAnd25db)
    t60Fromt20 = ((-60 - b25) / m25) / fs
    m35, b35 = linearRegression(signalBetween5dbAnd35db)
    t60Fromt30 = ((-60 - b35) / m35) / fs

    return t60Fromt10, t60Fromt20, t60Fromt30, edt




if __name__ == "__main__":
    from logarithmicScaleConversion import logarithmicScaleConversion
    from linearRegression import linearRegression
    from movingAverageFilter import movingAverageFilter
    from functions import getWAVData, plot, createFigure
    from pathlib import Path
    import yaml
    script_dir = Path(__file__).parent
    config_path = script_dir / 'config.yaml'

    with config_path.open("r") as file:
        config = yaml.safe_load(file)
        T60Array = config['T60Array']

    impulseResponse, time = getWAVData("impulse_responses/hamilton-mausoleum/b-format/hm2_000_bformat_48k.wav")

    impulseResponseLog = logarithmicScaleConversion(impulseResponse)

    plot(time, impulseResponseLog)

    smoothedImpulseResponseLog = movingAverageFilter(impulseResponseLog, 20)

    fig, ax = createFigure(time, smoothedImpulseResponseLog, title="IR between -5 and -35db")

    smoothedImpulseResponseLog5to35db, m, b = getAcousticParameters(smoothedImpulseResponseLog)

    timeSmoothedImpulseResponseLog5to35db5to35db = time[:len(smoothedImpulseResponseLog5to35db)]
    ax.plot(timeSmoothedImpulseResponseLog5to35db5to35db, smoothedImpulseResponseLog5to35db, label='Processed Signal', color='red')

    regressionLine = m * np.arange(len(smoothedImpulseResponseLog)) + b

    ax.plot(time, regressionLine, label='Regression Line', color='blue', linestyle='--')

    ax.set_ylim([-70, 0])
    plt.show()

    
            
