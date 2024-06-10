import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('')

from util.linearRegression import linearRegression

def getAcousticParameters(signal, fs):

    signalAbove5db = None
    signalBetween5dbAnd35db = None
    signalBetween5dbAnd25db = None
    signalBetween5dbAnd15db = None
    edt = None

    for i in range(len(signal) - 1000):
        if signal[i] <= -5 and signalAbove5db is None:
            if np.all(signal[i:i + 1000] <= -5):
                signalAbove5db = signal[i:]
                time5dbIndex = i

        if signal[i] <= -10 and edt is None:
            if np.all(signal[i:i + 1000] <= -10):
                time10dbIndex = i

        if signal[i] <= -15 and signalBetween5dbAnd15db is None:
            if np.all(signal[i:i + 1000] <= -15):
                signalBetween5dbAnd15db = signalAbove5db[:i]
                time15dbIndex = i
        
        if signal[i] <= -25 and signalBetween5dbAnd25db is None:
            if np.all(signal[i:i + 1000] <= -25):
                signalBetween5dbAnd25db = signalAbove5db[:i]
                time25dbIndex = i

        if signal[i] <= -35 and signalBetween5dbAnd35db is None:
            if np.all(signal[i:i + 1000] <= -35):
                signalBetween5dbAnd35db = signalAbove5db[:i]
                time35dbIndex = i
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

    m10, b10 = linearRegression(signal[:time10dbIndex + 1])
    edt = ((-60 - b10) / m10) / fs
    m15, b15 = linearRegression(signal[time5dbIndex:time15dbIndex + 1])
    b15 = b15 - (m15 * time5dbIndex)
    t60Fromt10 = ((-60 - b15) / m15) / fs
    m25, b25 = linearRegression(signal[time5dbIndex:time25dbIndex + 1])
    b25 = b25 - (m25 * time5dbIndex)
    t60Fromt20 = ((-60 - b25) / m25) / fs
    m35, b35 = linearRegression(signal[time5dbIndex:time35dbIndex + 1])
    b35 = b35 - (m35 * time5dbIndex)
    t60Fromt30 = ((-60 - b35) / m35) / fs

    return [t60Fromt10, t60Fromt20, t60Fromt30, edt]

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

    
            
