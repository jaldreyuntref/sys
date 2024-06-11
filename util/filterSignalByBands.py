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


if __name__ == "__main__":
    from synthesizeImpulseResponse import synthesizeImpulseResponse
    from pathlib import Path
    import yaml

    script_dir = Path(__file__).parent
    config_path = script_dir / '..' / 'util' / 'config.yaml'

    with config_path.open("r") as file:
        config = yaml.safe_load(file)
        octaveFrequencies = config["octaveFrequencies"]

    impulseResponse,time = synthesizeImpulseResponse(test=True)
    filterSignalByBands(impulseResponse, octaveFrequencies, 96000, "testing-data")
    print("Filtered synthesized impulse response in testing-data/filtered-ir.")