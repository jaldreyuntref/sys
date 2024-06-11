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

    return [t60Fromt10, t60Fromt20, t60Fromt30, edt], [[m15, b15], [m25, b25], [m35, b35]], [time5dbIndex, time15dbIndex, time25dbIndex, time35dbIndex]

if __name__ == "__main__":
    from logarithmicScaleConversion import logarithmicScaleConversion
    from synthesizeImpulseResponse import synthesizeImpulseResponse
    from hilbertTransform import hilbertTransform
    from movingAverageFilter import movingAverageFilter
    from schroederIntegral import schroederIntegral
    from functions import createFigure

    impuseResponse, time = synthesizeImpulseResponse(test=True)
    smoothedImpulseResponse = movingAverageFilter(hilbertTransform(impuseResponse), 2200)
    schroederIntegralOfSmoothedImpulseResponse = schroederIntegral(smoothedImpulseResponse)
    schroederIntegralOfSmoothedImpulseResponseLog = logarithmicScaleConversion(smoothedImpulseResponse)
    acousticParameters, regressionLinesValues, timeIndexes = getAcousticParameters(schroederIntegralOfSmoothedImpulseResponseLog, 44100)

    print("T60 from T10: ", acousticParameters[0])
    print("T60 from T20: ", acousticParameters[1])
    print("T60 from T30: ", acousticParameters[2])
    print("EDT: ", acousticParameters[3])

    m15 = regressionLinesValues[0][0]
    b15 = regressionLinesValues[0][1]
    m25 = regressionLinesValues[1][0]
    b25 = regressionLinesValues[1][1]
    m35 = regressionLinesValues[2][0]
    b35 = regressionLinesValues[2][1]

    time5dbIndex = timeIndexes[0]
    time15dbIndex = timeIndexes[1]
    time25dbIndex = timeIndexes[2]
    time35dbIndex = timeIndexes[3]

    fig, ax = createFigure(time, schroederIntegralOfSmoothedImpulseResponseLog, yLabel = "Amplitude (dB)", title = "Schroeder Integral Of Smoothed IR in Log scale")

    regressionLineT10 = m15 * (np.arange(len(schroederIntegralOfSmoothedImpulseResponseLog))) + b15 
    regressionLineT20 = m25 * (np.arange(len(schroederIntegralOfSmoothedImpulseResponseLog))) + b25 
    regressionLineT30 = m35 * (np.arange(len(schroederIntegralOfSmoothedImpulseResponseLog))) + b35 

    ax.plot(time, regressionLineT10, label='Regression Line T10', color='green', linestyle='--')
    ax.plot(time, regressionLineT20, label='Regression Line T20', color='blue', linestyle='--')
    ax.plot(time, regressionLineT30, label='Regression Line T30', color='brown', linestyle='--')

    ax.axvline(x=time[time5dbIndex], color='red', linestyle='--', label='Time 5dB Index')
    ax.axvline(x=time[time15dbIndex], color='green', linestyle='--', label='Time 15dB Index')
    ax.axvline(x=time[time25dbIndex], color='blue', linestyle='--', label='Time 25dB Index')
    ax.axvline(x=time[time35dbIndex], color='brown', linestyle='--', label='Time 35dB Index')

    ax.set_xlim([0, 1])
    ax.set_ylim([-65, 5])
    ax.legend()

    plt.show()


    
            
