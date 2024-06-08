import sys
sys.path.append('')

from util.functions import plot, askBooleanInput, plotWAV, getWAVData, plotDataFrame, createFigure, getDataFrameData

from util.logarithmicScaleConversion import logarithmicScaleConversion
from util.getAcousticParameters import getAcousticParameters
from util.movingAverageFilter import movingAverageFilter
from util.schroederIntegral import schroederIntegral
from util.filterSignalByBands import filterSignalByBands
from util.hilbertTransform import hilbertTransform
from util.synthesizeImpulseResponse import synthesizeImpulseResponse

from pathlib import Path
import yaml
import matplotlib.pyplot as plt
import numpy as np
#script_dir = Path(__file__).parent
#config_path = script_dir / 'config.yaml'

#with config_path.open("r") as file:
#    config = yaml.safe_load(file)

impulseResponse, time = getWAVData("impulse_responses/hamilton-mausoleum/b-format/hm2_000_bformat_48k.wav")

plot(time, impulseResponse, title="Impulse Response")

smoothedImpulseResponse = hilbertTransform(impulseResponse)
smoothedImpulseResponse = movingAverageFilter(impulseResponse, 1000)

plot(time, smoothedImpulseResponse, title="Smoothed Impulse Response")

schroederIntegralOfSmoothedImpulseResponse = schroederIntegral(smoothedImpulseResponse)

plot(time, schroederIntegralOfSmoothedImpulseResponse, title = "Schroeder Integral Of Smoothed IR")

schroederIntegralOfSmoothedImpulseResponseLog = logarithmicScaleConversion(schroederIntegralOfSmoothedImpulseResponse)

t60Fromt10, t60Fromt20, t60Fromt30, edt = getAcousticParameters(schroederIntegralOfSmoothedImpulseResponseLog)

print("t60Fromt10: ", t60Fromt10)
print("t60Fromt20: ", t60Fromt20)
print("t60Fromt30: ", t60Fromt30)
print("EDT: ", edt)

plot(time, schroederIntegralOfSmoothedImpulseResponseLog, yLabel = "Amplitude (dB)", title = "Schroeder Integral Of Smoothed IR in Log scale")

