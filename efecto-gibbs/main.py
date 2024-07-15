from harmonics import calculateFourierCoefficients, reconstructWave
from sawtooth import sawtooth
from triangle import triangle
from ecm import calculateECM
from gibbs import gibbs

import numpy as np
import matplotlib.pyplot as plt

print("Reconstruir la señal diente se sierra para 10, 20 y 50 armónicos...")

frequency = 1
samplingRate = 44100
duration = 5

sawtoothWave, time = sawtooth(frequency, samplingRate, duration)

a0, an, bn = calculateFourierCoefficients(sawtoothWave, time, 10, T=1/frequency)
reconstructedWave10 = reconstructWave(a0, an, bn, time, 10, T=1/frequency)

a0, an, bn = calculateFourierCoefficients(sawtoothWave, time, 20, T=1/frequency)
reconstructedWave20 = reconstructWave(a0, an, bn, time, 20, T=1/frequency)

a0, an, bn = calculateFourierCoefficients(sawtoothWave, time, 50, T=1/frequency)
reconstructedWave50 = reconstructWave(a0, an, bn, time, 50, T=1/frequency)


plt.figure(figsize=(10, 10))

plt.subplot(4, 1, 1)
plt.plot(time, sawtoothWave, label='Diente de sierra original')
plt.title('Diente de sierra original')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(time, reconstructedWave10, label='Diente de sierra reconstruida N = 10', color='orange')
plt.title('Diente de sierra reconstruida N = 10')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(time, reconstructedWave20, label='Diente de sierra reconstruida N = 20', color='orange')
plt.title('Diente de sierra reconstruida N = 20')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(time, reconstructedWave50, label='Diente de sierra reconstruida N = 50', color='orange')
plt.title('Diente de sierra reconstruida N = 50')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

print("Calcular ECM en puntos de continuidad...")
samplesInOnePeriod = int(((1/frequency) * samplingRate))

timeOnePeriod = np.linspace(0, 1/frequency, samplesInOnePeriod)
sawtoothPeriod = sawtoothWave[ int(samplesInOnePeriod / 2) : int(samplesInOnePeriod / 2 + samplesInOnePeriod)]
sawtoothPeriod10 = reconstructedWave10[ int(samplesInOnePeriod / 2) : int(samplesInOnePeriod / 2 + samplesInOnePeriod)]
sawtoothPeriod20 = reconstructedWave20[ int(samplesInOnePeriod / 2) : int(samplesInOnePeriod / 2 + samplesInOnePeriod)]
sawtoothPeriod50 = reconstructedWave50[ int(samplesInOnePeriod / 2) : int(samplesInOnePeriod / 2 + samplesInOnePeriod)]

sawtoothPeriod10ECM = calculateECM(sawtoothPeriod, sawtoothPeriod10)
sawtoothPeriod20ECM = calculateECM(sawtoothPeriod, sawtoothPeriod20)
sawtoothPeriod50ECM = calculateECM(sawtoothPeriod, sawtoothPeriod50)

plt.figure(figsize=(10, 10))

plt.subplot(4, 1, 1)
plt.plot(timeOnePeriod, sawtoothPeriod, label='Diente de sierra original')
plt.title('Diente de sierra original')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(timeOnePeriod, sawtoothPeriod10, label='Diente de sierra reconstruida N = 10', color='orange')
plt.title(f'Diente de sierra reconstruida N = 10\nECM = {sawtoothPeriod10ECM:.4f}')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(timeOnePeriod, sawtoothPeriod20, label='Diente de sierra reconstruida N = 20', color='orange')
plt.title(f'Diente de sierra reconstruida N = 20\nECM = {sawtoothPeriod20ECM:.4f}')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(timeOnePeriod, sawtoothPeriod50, label='Diente de sierra reconstruida N = 50', color='orange')
plt.title(f'Diente de sierra reconstruida N = 50\nECM = {sawtoothPeriod50ECM:.4f}')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()


print("Reconstruir la señal diente de sierra hasta que el ECM supere cierto umbral...")

thresholdECM = float(input("Ingrese un umbral para el ECM: "))
maxHarmonics = 100
currentHarmonic = 1
ECM = float('inf')
errors = []

while currentHarmonic <= maxHarmonics and ECM > thresholdECM:
    a0, an, bn = calculateFourierCoefficients(sawtoothWave, time, currentHarmonic, T=1/frequency)
    reconstructedWave = reconstructWave(a0, an, bn, time, currentHarmonic, T=1/frequency)
    
    ECM = calculateECM(sawtoothWave, reconstructedWave)
    errors.append(ECM)

    currentHarmonic += 1

plt.figure(figsize=(10, 8))

plt.subplot(3, 1, 1)
plt.plot(time, sawtoothWave, label='Diente de sierra original')
plt.title('Diente de sierra original')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(time, reconstructedWave, label=f'Diente de sierra reconstruida N = {currentHarmonic - 1}', color='orange')
plt.title(f'Diente de sierra reconstruida N = {currentHarmonic - 1}')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(range(1, currentHarmonic), errors, label='Error cuadrático medio')
plt.title('Error cuadrático medio vs Número de armónicos')
plt.xlabel('Número de armónicos')
plt.ylabel('Error cuadrático medio')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

print(f'ECM final: {errors[-1]}, N armónicos usados: {currentHarmonic - 1}')

print("Calcular el fenómeno de Gibbs...")
amountHarmonics = int(input("Ingrese la cantidad de armónicos: "))

a0, an, bn = calculateFourierCoefficients(sawtoothWave, time, amountHarmonics, T=1/frequency)
reconstructedWaveGibbs = reconstructWave(a0, an, bn, time, amountHarmonics, T=1/frequency)

gibbs(sawtoothWave, reconstructedWaveGibbs, samplingRate, frequency)

print("Repetir proceso para una señal triangular...")

triangleWave, time = triangle(frequency, samplingRate, duration)

print("Reconstruir la señal triangular para 10, 20 y 50 armónicos...")

a0, an, bn = calculateFourierCoefficients(triangleWave, time, 10, T=1/frequency)
reconstructedWave10 = reconstructWave(a0, an, bn, time, 10, T=1/frequency)

a0, an, bn = calculateFourierCoefficients(triangleWave, time, 20, T=1/frequency)
reconstructedWave20 = reconstructWave(a0, an, bn, time, 20, T=1/frequency)

a0, an, bn = calculateFourierCoefficients(triangleWave, time, 50, T=1/frequency)
reconstructedWave50 = reconstructWave(a0, an, bn, time, 50, T=1/frequency)


plt.figure(figsize=(10, 10))

plt.subplot(4, 1, 1)
plt.plot(time, triangleWave, label='Señal triangular original')
plt.title('Señal triangular original')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(time, reconstructedWave10, label='Señal triangular reconstruida N = 10', color='orange')
plt.title('Señal triangular reconstruida N = 10')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(time, reconstructedWave20, label='Señal triangular reconstruida N = 20', color='orange')
plt.title('Señal triangular reconstruida N = 20')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(time, reconstructedWave50, label='Señal triangular reconstruida N = 50', color='orange')
plt.title('Señal triangular reconstruida N = 50')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

print("Reconstruir la señal triangular hasta que el ECM supere cierto umbral...")

thresholdECM = float(input("Ingrese un umbral para el ECM: "))
maxHarmonics = 100
currentHarmonic = 1
ECM = float('inf')
errors = []

while currentHarmonic <= maxHarmonics and ECM > thresholdECM:
    a0, an, bn = calculateFourierCoefficients(triangleWave, time, currentHarmonic, T=1/frequency)
    reconstructedWave = reconstructWave(a0, an, bn, time, currentHarmonic, T=1/frequency)
    
    ECM = calculateECM(triangleWave, reconstructedWave)
    errors.append(ECM)

    currentHarmonic += 1

plt.figure(figsize=(10, 8))

plt.subplot(3, 1, 1)
plt.plot(time, triangleWave, label='Diente de sierra original')
plt.title('Diente de sierra original')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(time, reconstructedWave, label=f'Diente de sierra reconstruida N = {currentHarmonic - 1}', color='orange')
plt.title(f'Diente de sierra reconstruida N = {currentHarmonic - 1}')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(range(1, currentHarmonic), errors, label='Error cuadrático medio')
plt.title('Error cuadrático medio vs Número de armónicos')
plt.xlabel('Número de armónicos')
plt.ylabel('Error cuadrático medio')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

print(f'ECM final: {errors[-1]}, N armónicos usados: {currentHarmonic - 1}')

print("Calcular el fenómeno de Gibbs...")
amountHarmonics = int(input("Ingrese la cantidad de armónicos: "))

a0, an, bn = calculateFourierCoefficients(triangleWave, time, amountHarmonics, T=1/frequency)
reconstructedWaveGibbs = reconstructWave(a0, an, bn, time, amountHarmonics, T=1/frequency)

gibbs(triangleWave, reconstructedWaveGibbs, samplingRate, frequency)