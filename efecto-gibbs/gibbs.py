import numpy as np

def gibbs(wave, reconstructedWave, samplingRate, frequency):
    discontinuity_index = np.argmax(np.diff(wave))
    overshoot = np.max(reconstructedWave[discontinuity_index:discontinuity_index + samplingRate//frequency])

    D = 2
    gibbsTheoretical = 0.0895 * D

    # Calcular el error cometido
    gibbsMeasured = overshoot - np.max(wave)
    errorPercentage = (gibbsMeasured / gibbsTheoretical) * 100

    # Imprimir resultados
    print(f'Teórico Gibbs Overshoot: {gibbsTheoretical}')
    print(f'Medido Gibbs Overshoot: {gibbsMeasured}')
    print(f'Error cometido: {errorPercentage}%')