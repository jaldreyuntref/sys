import sys
sys.path.append('')

from util.functions import getWAVData, plot, createFigure, overwriteYAML

from util.logarithmicScaleConversion import logarithmicScaleConversion
from util.getAcousticParameters import getAcousticParameters
from util.movingAverageFilter import movingAverageFilter
from util.schroederIntegral import schroederIntegral
from util.filterSignalByBands import filterSignalByBands
from util.hilbertTransform import hilbertTransform
from util.synthesizeImpulseResponse import synthesizeImpulseResponse
from util.getC80 import getC80
from util.getD50 import getD50
from util.saveFiles import saveFiles

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

impulseResponses = []

# preguntar si quiere carga la IR
impulseResponseRoutes = saveFiles()
for impulseResponseRoute in impulseResponseRoutes:
    impulseResponse, time, sampleRateFromWAV = getWAVData(impulseResponseRoute)
    impulseResponses.append([impulseResponse, time, sampleRateFromWAV, Path(impulseResponseRoute).stem])

# preguntar si quiere sintetizar la IR

# preguntar si quiere obtener la IR

for impulseResponseArray in impulseResponses:
    impulseResponse = impulseResponseArray[0]
    time = impulseResponseArray[1]
    sampleRate = impulseResponseArray[2]
    impulseResponseName = impulseResponseArray[3]

    newFolderPath = script_dir / impulseResponseName
    newFolderPath.mkdir(parents=True, exist_ok=True)

    filteredImpulseResponsesPath = script_dir / impulseResponseName / "filtered-ir"
    filteredImpulseResponsesPath.mkdir(parents=True, exist_ok=True)

    acousticParametersTextFilePath = newFolderPath / "acoustic-parameters.txt"
    acousticParametersTextFilePath.touch(exist_ok=True)

    # preguntar cuales quiere que sean la frecuencias centrales
    filterFrequencies = octaveFrequencies
    filterFrequencies = filterFrequencies[2:9] if len(filterFrequencies) == 10 else filterFrequencies[7:26]

    filteredSignalArray = filterSignalByBands(impulseResponse, filterFrequencies, sampleRate, impulseResponseName)

    frequencyCounter = 0
    for impulseResponse in filteredSignalArray:
        currentFrequency = filterFrequencies[frequencyCounter]
        #plot(time, impulseResponse, title="Impulse Response")

        smoothedImpulseResponse = hilbertTransform(impulseResponse)
        smoothedImpulseResponse = movingAverageFilter(smoothedImpulseResponse, 24000)

        c80 = getC80(impulseResponse, sampleRate)
        d50 = getD50(impulseResponse, sampleRate)

        #plot(time, smoothedImpulseResponse, title="Smoothed Impulse Response")

        schroederIntegralOfSmoothedImpulseResponse = schroederIntegral(smoothedImpulseResponse)

        #plot(time, schroederIntegralOfSmoothedImpulseResponse, title = "Schroeder Integral Of Smoothed IR")

        schroederIntegralOfSmoothedImpulseResponseLog = logarithmicScaleConversion(schroederIntegralOfSmoothedImpulseResponse)

        acousticParameters  = getAcousticParameters(schroederIntegralOfSmoothedImpulseResponseLog, sampleRate)

        with acousticParametersTextFilePath.open("a") as file:
            file.write(f"\nAcoustic Parameters {currentFrequency}Hz:\n")
            file.write("====================\n")
            file.write(f"T60 from T10: {acousticParameters[0]}\n")
            file.write(f"T60 from T20: {acousticParameters[1]}\n")
            file.write(f"T60 from T30: {acousticParameters[2]}\n")
            file.write(f"EDT: {acousticParameters[3]}\n")
            file.write(f"C80: {c80}\n")
            file.write(f"D50: {d50}\n")

        frequencyCounter += 1

        #fig, ax = createFigure(time, schroederIntegralOfSmoothedImpulseResponseLog, yLabel = "Amplitude (dB)", title = "Schroeder Integral Of Smoothed IR in Log scale")
        #regression_line = m35 * (np.arange(len(schroederIntegralOfSmoothedImpulseResponseLog))) + b35 
        #ax.plot(time, logarithmicScaleConversion(smoothedImpulseResponse), label="RMS", color="green")
        #ax.plot(time, regression_line, label='Regression Line', color='blue', linestyle='--')

        #ax.axvline(x=time[time5dbIndex], color='red', linestyle='--', label='Time 5dB Index')
        #ax.axvline(x=time[time35dbIndex], color='green', linestyle='--', label='Time 35dB Index')

        plt.show()

