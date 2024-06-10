import sys
sys.path.append('')

from util.functions import getWAVData, plot, createFigure, askBooleanInput, askOctaveOrThridsInput

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
from util.pinkNoise import pinkNoise
from util.generateSineSweepInverseFilter import generateSineSweepInverseFilter
from util.adquisitionReproduction import adquisitionReproduction

from pathlib import Path
import yaml
import matplotlib.pyplot as plt
import numpy as np

script_dir = Path(__file__).parent
config_path = script_dir / '..' / 'util' / 'config.yaml'

with config_path.open("r") as file:
    config = yaml.safe_load(file)
    octaveFrequencies = config["octaveFrequencies"]
    thirdsFrequencies = config["thirdsFrequencies"]


impulseResponses = []

# Load IR
loadImpulseResponsesBoolean = askBooleanInput("Do you want to load impulse responses from file directory? (only .WAV files permitted)")
if loadImpulseResponsesBoolean:
    impulseResponseRoutes = saveFiles()
    for impulseResponseRoute in impulseResponseRoutes:
        impulseResponse, time, sampleRateFromWAV = getWAVData(impulseResponseRoute)
        impulseResponses.append([impulseResponse, time, sampleRateFromWAV, Path(impulseResponseRoute).stem])

# Synthesize IR
synthesizeImpulseResponsesBoolean = askBooleanInput("Do you want to synthesize and impulse response based on its T60 values?")
if synthesizeImpulseResponsesBoolean:
    sampleRate = int(input("Enter a sampling rate: "))
    octaveOrThirdsInput = askOctaveOrThridsInput("Synthesize impulse response based on octaves or thirds?")
    synthesizeT60Frequencies = octaveFrequencies if octaveOrThirdsInput == 'octave' else thirdsFrequencies
    T60Array = []
    for frequency in synthesizeT60Frequencies:
        T60Value = float(input(f"T60 value for {frequency}Hz: "))
        T60Array.append(T60Value)
    provideAmplitudeValuesBoolean = askBooleanInput("Do you want to provide an specific amplitude for each frequency?")
    if provideAmplitudeValuesBoolean:
        T60AmplitudeArray = []
        for frequency in synthesizeT60Frequencies:
            T60AmplitudeValue = float(input(f"T60 amplitude value for {frequency}Hz: "))
            T60AmplitudeArray.append(T60AmplitudeValue)
    else:
        T60AmplitudeArray = 1
    durationSynthesizedImpulseResponse = int(input("Enter the duration of the synthesized impulse response: "))
    impulseResponse, time = synthesizeImpulseResponse(T60Array, durationSynthesizedImpulseResponse, octaveOrThirdsInput, T60AmplitudeArray, sampleRate)
    impulseResponses.append([impulseResponse, time, sampleRate, "synthesized-ir"])


# Obtain IR
synthesizeImpulseResponsesBoolean = askBooleanInput("Do you want to obtain an impulse response providing a sine sweep and an inverse filter?")
if synthesizeImpulseResponsesBoolean:
    provideSineSweepInverseFilterPinkNoiseBoolean = askBooleanInput("Do you need a sine sweep, inverse filter and pink noise to perform the measurement?")
    if provideSineSweepInverseFilterPinkNoiseBoolean:
        sampleRate = int(input("Enter a sampling rate: "))
        pinkNoiseDuration = int(input("Enter the duration of the pink noise: "))
        pinkNoise(pinkNoiseDuration, sampleRate)
        lowerFrequencySineSweep = int(input("Enter a starting frequency for the sine sweep: "))
        upperFrequencySineSweep = int(input("Enter a final frequency for the sine sweep: "))
        sineSweepInverseFilterDuration = int(input("Enter the duration of the sine sweep and inverse filter: "))
        generateSineSweepInverseFilter(lowerFrequencySineSweep, upperFrequencySineSweep, sineSweepInverseFilterDuration, sampleRate)
        readyToBeginAdquisitionReproduction = askBooleanInput("Ready to begin the process of obtaining the impulse response?")
        if readyToBeginAdquisitionReproduction:
            adquisitionReproduction()

        

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

