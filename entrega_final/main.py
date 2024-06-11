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
from util.getImpulseResponse import getImpulseResponse
from util.generateImpulseResponseDirectory import generateImpulseResponseDirectory

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
        acousticParametersTextFilePath = generateImpulseResponseDirectory(script_dir, Path(impulseResponseRoute).stem)
        impulseResponses.append([impulseResponse, time, sampleRateFromWAV, Path(impulseResponseRoute).stem, acousticParametersTextFilePath])

# Synthesize IR
if impulseResponses == []:
    synthesizeImpulseResponsesBoolean = askBooleanInput("Do you want to synthesize an impulse response based on its T60 values?")
    if synthesizeImpulseResponsesBoolean:
        synthesizedImpulseResponseName = input("Please provide a name for the impulse response, generated folders and files will be based in this name: ")
        acousticParametersTextFilePath = generateImpulseResponseDirectory(script_dir, synthesizedImpulseResponseName)
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
        impulseResponse, time = synthesizeImpulseResponse(T60Array, durationSynthesizedImpulseResponse, synthesizeT60Frequencies, T60AmplitudeArray, sampleRate, synthesizedImpulseResponseName)
        impulseResponses.append([impulseResponse, time, sampleRate, synthesizedImpulseResponseName, acousticParametersTextFilePath])

# Obtain IR
if impulseResponses == []:
    synthesizeImpulseResponsesBoolean = askBooleanInput("Do you want to obtain an impulse response providing a sine sweep and an inverse filter?")
    if synthesizeImpulseResponsesBoolean:
        obtainedImpulseResponseName = input("Please provide a name for the impulse response, generated folders and files will be based in this name: ")
        acousticParametersTextFilePath = generateImpulseResponseDirectory(script_dir, obtainedImpulseResponseName)
        provideSineSweepInverseFilterPinkNoiseBoolean = askBooleanInput("Do you need a sine sweep, inverse filter and pink noise to perform the measurement?")
        if provideSineSweepInverseFilterPinkNoiseBoolean:
            sampleRate = int(input("Enter a sampling rate: "))
            pinkNoiseDuration = int(input("Enter the duration of the pink noise: "))
            pinkNoise(pinkNoiseDuration, sampleRate)
            lowerFrequencySineSweep = int(input("Enter a starting frequency for the sine sweep: "))
            upperFrequencySineSweep = int(input("Enter a final frequency for the sine sweep: "))
            sineSweepInverseFilterDuration = int(input("Enter the duration of the sine sweep and inverse filter: "))
            generateSineSweepInverseFilter(lowerFrequencySineSweep, upperFrequencySineSweep, sineSweepInverseFilterDuration, sampleRate)
            print("Sine sweep, inverse filter and pink noise generated in entrega_final/obtain-IR.")
            readyToBeginAdquisitionReproduction = askBooleanInput("Ready to begin the process of obtaining the impulse response?")
            if readyToBeginAdquisitionReproduction:
                adquisitionReproduction()
                print("Output of adquisition and reproduction generated in entrega_final/obtain-IR/output-adquisition-reproduction.wav.")
        print("Select the reproduced sine sweep.")
        sineSweepRoute = saveFiles(recursive=False)[0]
        print("Select the invese filter.")
        inverseFilterRoute = saveFiles(recursive=False)[0]
        sineSweep, timeSineSweep, sampleRateSineSweep = getWAVData(sineSweepRoute)
        inverseFilter, timeInverseFilter, sampleRateInverseFilter= getWAVData(inverseFilterRoute)
        if sampleRateSineSweep == sampleRateInverseFilter:
            impulseResponse = getImpulseResponse(sineSweep, inverseFilter)
            impulseResponseTime = np.linspace(0, len(impulseResponse) / sampleRateSineSweep, len(impulseResponse))
            impulseResponses.append([impulseResponse, impulseResponseTime, sampleRateSineSweep, obtainedImpulseResponseName, acousticParametersTextFilePath])
        else:
            print("The sampling rates of the sine sweep and inverse filter differ, please provide signals with equal sampling rates.")

if impulseResponses == []:
    print("There are no impulse responses to analyze, please select one of the methods offered previously.")

saveGraphs = False
saveGraphs = askBooleanInput("Do you want to save graphs of the processed impulse response (it will increase processing time) ?")

for impulseResponseArray in impulseResponses:
    impulseResponse = impulseResponseArray[0]
    time = impulseResponseArray[1]
    sampleRate = impulseResponseArray[2]
    impulseResponseName = impulseResponseArray[3]
    acousticParametersTextFilePath = impulseResponseArray[4]

    octaveOrThirdsInput = askOctaveOrThridsInput(f"Filter {impulseResponseName} based on octaves or thirds?")
    filterFrequencies = octaveFrequencies if octaveOrThirdsInput == 'octave' else thirdsFrequencies
    filterFrequencies = filterFrequencies[2:9] if len(filterFrequencies) == 10 else filterFrequencies[7:26]

    filteredSignalArray = filterSignalByBands(impulseResponse, filterFrequencies, sampleRate, impulseResponseName)

    frequencyCounter = 0
    for impulseResponse in filteredSignalArray:
        currentFrequency = filterFrequencies[frequencyCounter]
        impulseResponse /= np.max(np.abs(impulseResponse))

        if saveGraphs:
            plot(time, impulseResponse, title=f"{impulseResponseName}-{currentFrequency}Hz", show=False, save=f"entrega_final/{impulseResponseName}/graphs/{impulseResponseName}-{currentFrequency}Hz.png")

        smoothedImpulseResponse = hilbertTransform(impulseResponse)
        smoothedImpulseResponse = movingAverageFilter(smoothedImpulseResponse, 44000)

        c80 = getC80(impulseResponse, sampleRate)
        d50 = getD50(impulseResponse, sampleRate)

        if saveGraphs:
            plot(time, smoothedImpulseResponse, title=f"Smoothed {impulseResponseName} - {currentFrequency}Hz", show=False, save=f"entrega_final/{impulseResponseName}/graphs/smoothed-{impulseResponseName}-{currentFrequency}Hz.png")

        schroederIntegralOfSmoothedImpulseResponse = schroederIntegral(smoothedImpulseResponse)

        if saveGraphs:
            plot(time, schroederIntegralOfSmoothedImpulseResponse, title = f"Schroeder Integral Of Smoothed {impulseResponseName} - {currentFrequency}Hz", show=False, save=f"entrega_final/{impulseResponseName}/graphs/schroeder-smoothed-{impulseResponseName}-{currentFrequency}Hz.png")

        schroederIntegralOfSmoothedImpulseResponseLog = logarithmicScaleConversion(schroederIntegralOfSmoothedImpulseResponse)

        acousticParameters, regressionLinesValues, timeIndexes  = getAcousticParameters(schroederIntegralOfSmoothedImpulseResponseLog, sampleRate)

        with acousticParametersTextFilePath.open("a") as file:
            file.write(f"\nAcoustic Parameters {currentFrequency}Hz:\n")
            file.write("====================\n")
            file.write(f"T60 from T10: {acousticParameters[0]}\n")
            file.write(f"T60 from T20: {acousticParameters[1]}\n")
            file.write(f"T60 from T30: {acousticParameters[2]}\n")
            file.write(f"EDT: {acousticParameters[3]}\n")
            file.write(f"C80: {c80}\n")
            file.write(f"D50: {d50}\n")

        if saveGraphs:
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

            fig.savefig(f'entrega_final/{impulseResponseName}/graphs/schroeder-smoothed-{impulseResponseName}-{currentFrequency}Hz-log.png', dpi=300, bbox_inches='tight')
            plt.close(fig)

        frequencyCounter += 1


