from sawtooth import sawtooth
from harmonics import calculateFourierCoefficients, reconstructWave

import numpy as np
import matplotlib.pyplot as plt

def gibbs(wave, reconstructedWave, samplingRate, frequency):
    discontinuityIndex = np.argmax(np.abs(np.diff(wave)))
    overshoot = np.max(reconstructedWave[discontinuityIndex:discontinuityIndex + samplingRate//frequency])

    discontinuityJump = np.abs(wave[discontinuityIndex + 1] - wave[discontinuityIndex])
    gibbsTheoretical = 0.0895 * discontinuityJump

    gibbsMeasured = overshoot - np.max(wave)
    errorPercentage = (1 - (gibbsMeasured / gibbsTheoretical)) * 100

    print(f'Teórico Gibbs Overshoot: {gibbsTheoretical}')
    print(f'Medido Gibbs Overshoot: {gibbsMeasured}')
    print(f'Error cometido: {errorPercentage}%')

    # Crear la figura y los subplots
    plt.figure(figsize=(10, 8))

    # Subplot 1: Señal original y señal reconstruida
    plt.subplot(3, 1, 1)
    plt.plot(wave, label='Señal original')
    plt.plot(reconstructedWave, label='Señal reconstruida', linestyle='--')
    plt.plot(discontinuityIndex, wave[discontinuityIndex], 'ro', label='Punto de discontinuidad')
    plt.title('Señal Original y Reconstruida')
    plt.xlabel('Muestras')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.legend()

    # Subplot 2: Overshoot medido en la señal reconstruida
    plt.subplot(3, 1, 2)
    plt.plot(reconstructedWave, label='Señal reconstruida')
    plt.plot(discontinuityIndex, overshoot, 'ro', label='Overshoot medido')
    plt.title('Señal Reconstruida y Overshoot Medido')
    plt.xlabel('Muestras')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.legend()

    # Subplot 3: Primera derivada de la señal original
    plt.subplot(3, 1, 3)
    diff_wave = np.diff(wave)
    plt.plot(diff_wave, label='Primera derivada de la señal original', color='g')
    plt.plot(discontinuityIndex, diff_wave[discontinuityIndex], 'ro', label='Punto de discontinuidad')
    plt.title('Primera Derivada de la Señal Original')
    plt.xlabel('Muestras')
    plt.ylabel('Diferencia')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    sawtoothWave, time = sawtooth()
    a0, an, bn = calculateFourierCoefficients(sawtoothWave, time, 1000, T=1/1)
    reconstructedWave50 = reconstructWave(a0, an, bn, time, 1000, T=1/1)
    gibbs(sawtoothWave, reconstructedWave50, 44100, 1)
