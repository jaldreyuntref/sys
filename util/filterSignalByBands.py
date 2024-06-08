def filterSignalByBands(audioData, band="octave"):

    """
    
    Filters a signal with a bandpass filter with different central frequencies, either by octave or thirds.

    Parameters:
        audioData(list): The audio signal to be filtered.
        band (string): The central frequencies, by default it is the central frequencies by octave band according to IEC61260 from 125Hz to 8000Hz.

    Returns:
        list: The list of filtered signals.
    
    """ 

    signals = []
    centralFrequencies = [125,250,500,1000,2000,4000,8000] if band == "octave" else [125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000,6300,8000]

    for frequency in centralFrequencies:
        #Octava - G = 1.0/2.0 / 1/3 de Octava - G=1.0/6.0
        G = 1.0/2.0 if band == "octave" else 1.0/6.0
        factor = np.power(2, G)
        centerFrequency_Hz = frequency

        #Calculo los extremos de la banda a partir de la frecuencia central
        lowerCutoffFrequency_Hz = centerFrequency_Hz / factor
        upperCutoffFrequency_Hz = centerFrequency_Hz * factor

        #print('Frecuencia de corte inferior: ', round(lowerCutoffFrequency_Hz), 'Hz')
        #print('Frecuencia de corte superior: ', round(upperCutoffFrequency_Hz), 'Hz')

        # Extraemos los coeficientes del filtro 
        #b,a = signal.iirfilter(4, [2*np.pi*lowerCutoffFrequency_Hz,2*np.pi*upperCutoffFrequency_Hz],
        #                            rs=60, btype='band', analog=True,
        #                            ftype='butter')

        # para aplicar el filtro es más óptimo
        sos = signal.iirfilter(4, [lowerCutoffFrequency_Hz,upperCutoffFrequency_Hz],
                                    rs=60, btype='band', analog=False,
                                    ftype='butter', fs=fs, output='sos')
        #w, h = signal.freqs(b,a)

        # aplicando filtro al audio
        signals.append(signal.sosfilt(sos, audioData))
    
    return signals