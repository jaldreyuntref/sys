import sys
sys.path.append('')

from util.functions import getWAVData, plot, createFigure

from util.logarithmicScaleConversion import logarithmicScaleConversion
from util.getAcousticParameters import getAcousticParameters
from util.movingAverageFilter import movingAverageFilter
from util.schroederIntegral import schroederIntegral
from util.filterSignalByBands import filterSignalByBands
from util.hilbertTransform import hilbertTransform
from util.synthesizeImpulseResponse import synthesizeImpulseResponse
from util.getC80 import getC80
from util.getD50 import getD50

from pathlib import Path
import yaml
import matplotlib.pyplot as plt
import numpy as np
script_dir = Path(__file__).parent
config_path = script_dir / '..' / 'util' / 'config.yaml'

with config_path.open("r") as file:
    config = yaml.safe_load(file)
    sampleRate = config["sampleRate"]
    octaveFrequencies = config["octaveFrequencies"]
    thirdsFrequencies = config["thirdsFrequencies"]
    T60Array = config["T60Array"]

impulseResponse, time, sampleRateFromWAV = getWAVData("impulse_responses/IR2-drive/Mono.wav")
sampleRate = sampleRateFromWAV

centralFrequencies = octaveFrequencies
impulseResponseName = "IR2-drive"

filteredSignalArray = filterSignalByBands(impulseResponse, centralFrequencies, sampleRate, impulseResponseName)

for impulseResponse in filteredSignalArray:
    print("---------------------------------------")
    #plot(time, impulseResponse, title="Impulse Response")

    smoothedImpulseResponse = hilbertTransform(impulseResponse)
    smoothedImpulseResponse = movingAverageFilter(smoothedImpulseResponse, 24000)

    c80 = getC80(impulseResponse, sampleRate)
    d50 = getD50(impulseResponse, sampleRate)

    #plot(time, smoothedImpulseResponse, title="Smoothed Impulse Response")

    schroederIntegralOfSmoothedImpulseResponse = schroederIntegral(smoothedImpulseResponse)

    #plot(time, schroederIntegralOfSmoothedImpulseResponse, title = "Schroeder Integral Of Smoothed IR")

    schroederIntegralOfSmoothedImpulseResponseLog = logarithmicScaleConversion(schroederIntegralOfSmoothedImpulseResponse)

    t60Fromt10, t60Fromt20, t60Fromt30, edt, m35, b35, time5dbIndex, time35dbIndex  = getAcousticParameters(schroederIntegralOfSmoothedImpulseResponseLog, sampleRate)

    print("t60Fromt10: ", t60Fromt10)
    print("t60Fromt20: ", t60Fromt20)
    print("t60Fromt30: ", t60Fromt30)
    print("EDT: ", edt)
    print("C80: ", c80)
    print("D50: ", d50)

    #fig, ax = createFigure(time, schroederIntegralOfSmoothedImpulseResponseLog, yLabel = "Amplitude (dB)", title = "Schroeder Integral Of Smoothed IR in Log scale")
    #regression_line = m35 * (np.arange(len(schroederIntegralOfSmoothedImpulseResponseLog))) + b35 
    #ax.plot(time, logarithmicScaleConversion(smoothedImpulseResponse), label="RMS", color="green")
    #ax.plot(time, regression_line, label='Regression Line', color='blue', linestyle='--')

    #ax.axvline(x=time[time5dbIndex], color='red', linestyle='--', label='Time 5dB Index')
    #ax.axvline(x=time[time35dbIndex], color='green', linestyle='--', label='Time 35dB Index')

    plt.show()

