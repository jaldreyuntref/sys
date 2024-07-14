from harmonics import calculateFourierCoefficients, reconstructWave
from sawtooth import sawtooth
from ecm import calculateECM

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

print(f'MSE final: {errors[-1]}, N armónicos usados: {currentHarmonic - 1}')