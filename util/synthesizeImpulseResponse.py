import numpy as np
from scipy.io import wavfile

from pathlib import Path
import yaml

script_dir = Path(__file__).parent
config_path = script_dir / '..' / 'util' / 'config.yaml'

with config_path.open("r") as file:
    config = yaml.safe_load(file)
    octaveFrequencies = config["octaveFrequencies"]
    T60Array = config["T60Array"]

def synthesizeImpulseResponse(t60 = T60Array, duration = 3, centralFrequencies = octaveFrequencies, a=1, fs=44100, synthesizedImpulseResponseName="synthesized-ir", test=False):

    """
        
        Synthesizes an impulse response based on a T60 values list for corresponding frequencies. It will also create the wav file in media/synthesized-impulse-response.wav.

        Parameters:
            t60 (list): The list of T60 values for each frequency, following the same order as the frequencies by octave or thirds.
            duration (float): The duration of the impulse response.
            band (string): A value that specifies if the impulse response will be synthesized based on a T60 for each frquency in a list of frequencies by octave or by thirds.
            a (float): Amplitude coefficient for each impulse response that compose the final impulse response. By default its value is 1, which will be interpreted as a 1 for all frequencies.
            fs (int): The sampling rate.

        Returns:
            list: The impulse response.
            list:  The time vector.

        """  
    if a == 1:
        a = np.ones(len(centralFrequencies))
    if len(a) != len(centralFrequencies) != len(t60):
        print("The length of the list of amplitude coefficients, central frequencies, and T60 values dont match. Please provide ones that do.")
        return
    t60 = np.array(t60)
    time = np.linspace(0, duration, duration*fs)
    impulseResponses = []
    for i in range(len(centralFrequencies)):
        tau = -np.log(10**(-3)) / t60[i]
        impulseResponses.append(a[i]*np.exp(-tau*time)*np.cos(2*np.pi*centralFrequencies[i]*time))

    impulseResponse = sum(impulseResponses)
    impulseResponse = impulseResponse / np.max(np.abs(impulseResponse))
    if test == False:
        wavfile.write(f"entrega_final/{synthesizedImpulseResponseName}/{synthesizedImpulseResponseName}.wav", fs, np.int16(impulseResponse * 32767))
    return impulseResponse, time


if __name__ == "__main__":
    from synthesizeImpulseResponse import synthesizeImpulseResponse
    from functions import plot

    impulseResponse,time = synthesizeImpulseResponse(test=True)
    plot(time, impulseResponse, title="synthesizeImpulseResponse result")