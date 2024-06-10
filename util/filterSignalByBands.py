import numpy as np
from scipy import signal
from scipy.io import wavfile

def filterSignalByBands(audioData, centralFrequencies, fs, impulseResponseName):

    """
    
    Filters a signal with a bandpass filter with different central frequencies, either by octave or thirds.

    Parameters:
        audioData(list): The audio signal to be filtered.
        band (string): The central frequencies, by default it is the central frequencies by octave band according to IEC61260 from 125Hz to 8000Hz.

    Returns:
        list: The list of filtered signals.
    
    """ 
    print(fs)
    print(impulseResponseName)
    signals = []

    for frequency in centralFrequencies:
        G = 1.0/2.0 if len(centralFrequencies) == 10 else 1.0/6.0
        factor = np.power(2, G)
        centerFrequency_Hz = frequency

        lowerCutoffFrequency_Hz = centerFrequency_Hz / factor
        upperCutoffFrequency_Hz = centerFrequency_Hz * factor

        sos = signal.iirfilter(4, [lowerCutoffFrequency_Hz,upperCutoffFrequency_Hz],
                                    rs=60, btype='band', analog=False,
                                    ftype='butter', fs=fs, output='sos')

        filteredSignal = signal.sosfilt(sos, audioData)
        signals.append(filteredSignal)

        filename = f"entrega_final/{impulseResponseName}/filtered-ir/filtered-ir-{int(centerFrequency_Hz)}Hz.wav"
        wavfile.write(filename, fs, np.int16(filteredSignal * 32767))
    
    return signals