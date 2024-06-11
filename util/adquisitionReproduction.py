import pyaudio
import wave

def adquisitionReproduction():

    """
    Performs simultaneous audio acquisition and reproduction for a specified duration.

    This function allows recording audio from a user-selected input device and simultaneously 
    playing it back through a user-selected output device. It saves the output as a .WAV file 
    in entrega_final/obtain-IR/output-adquisition-reproduction.wav.

    """

    pyaudio_instance = pyaudio.PyAudio()
    device_count = pyaudio_instance.get_device_count()

    print("Available audio devices:")
    for i in range(device_count):
        device_info = pyaudio_instance.get_device_info_by_index(i)
        print(f"{i}: {device_info['name']}")

    selected_input_device_index = int(input("Select the input devices based of its index number: "))
    selected_input_device = pyaudio_instance.get_device_info_by_index(selected_input_device_index)

    selected_output_device_index = int(input("Select the output devices based of its index number: "))
    selected_output_device = pyaudio_instance.get_device_info_by_index(selected_output_device_index)

    seconds = int(input("Enter the duration of the process: "))

    input_stream = pyaudio_instance.open(
        channels=1,   
        format=pyaudio.paInt16, 
        input=True, 
        input_device_index=selected_input_device_index, 
        rate=int(selected_input_device['defaultSampleRate']), 
        frames_per_buffer=1024
    )

    output_stream = pyaudio_instance.open(
        channels=1,   
        format=pyaudio.paInt16, 
        output=True,
        input=True, 
        output_device_index=selected_output_device_index, 
        rate=int(selected_output_device['defaultSampleRate']), 
        frames_per_buffer=1024
    )
    
    inputFrames = []
    outputFrames = []

    for i in range(0, int(selected_input_device['defaultSampleRate'] / 1024 * seconds)):
        inputData = input_stream.read(1024)
        output_stream.write(inputData)
        outputData = output_stream.read(1024)

        inputFrames.append(inputData)
        outputFrames.append(outputData)

    input_stream.stop_stream()
    input_stream.close()

    output_stream.stop_stream()
    output_stream.close()
    
    pyaudio_instance.terminate()

    wfOutput = wave.open("entrega_final/obtain-IR/output-adquisition-reproduction.wav", 'wb')
    wfOutput.setnchannels(1)
    wfOutput.setsampwidth(pyaudio_instance.get_sample_size(pyaudio.paInt16))
    wfOutput.setframerate(selected_input_device['defaultSampleRate'])
    wfOutput.writeframes(b''.join(outputFrames))
    wfOutput.close()

if __name__ == "__main__":
    adquisitionReproduction()
