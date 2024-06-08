import numpy as np
from scipy.io import wavfile

def synthesizeImpulseResponse(t60, duration = 3, band="octave", a=1, fs=44100):

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

    centralFrequencies = [31.5,63,125,250,500,1000,2000,4000,8000,16000] if band == "octave" else [25,31.5,40,50,63,80,100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000,6300,8000,10000,12500,16000,20000]
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
    #wavfile.write("media/synthesized-impulse-response.wav", fs, np.int16(impulseResponse * 32767))
    return impulseResponse, time