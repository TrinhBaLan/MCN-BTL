from scipy.io.wavfile import read, write, WavFileWarning
import matplotlib.pyplot as plt
import numpy as np

def read_audio_file(path):
    """
    Read a WAV file and return its sample rate and numpy array containing audio data
    :param path: File to be read
    """
    try:
        samplerate, data = read(path)
        print(f"Sample rate: {samplerate} Hz")
        print("Number of channels in this file: ", 1 if len(data.shape) == 1 else data.shape[1])
        return samplerate, data
    except FileNotFoundError:
        print(f"Your requested file '{path}' does not exist. Try again.")
    except WavFileWarning:
        print("There seems to be a problem reading your WAV file.")

def write_audio_file(path, samplerate, transformed_data):
    """
    Write spectified audio data to a WAV file
    :param path: File location
    :param samplerate: Sample rate of the data
    :param data: Audio data as numpy array
    """
    try:
        # See how many channel we got. Then write to output file
        if len(transformed_data) == 1:
            write(path, samplerate, transformed_data[0])
        else:
            left_channel = transformed_data[0]
            right_channel = transformed_data[1]
            output = []
            for i in range(len(left_channel)):
                output.append(np.array(left_channel[i], right_channel[i]))
            write(path, samplerate, np.array(output))

    except WavFileWarning:
        print("There seems to be a problem reading your WAV file.")

def plot_waveform(length, data, data_label):
    """
    Plot the specified data
    :param length: Length of the audio file
    :param data: Audio data as numpy array
    """
    time = np.linspace(0., length, data.shape[0])
    plt.title("Graph of audio signal")
    plt.plot(time, data, label=data_label)
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.savefig("graph.png")

def mse_eval(data, reconstructed_data):
    sum = 0.0
    for i  in range (0, len(data)):
        sum += (int(reconstructed_data[i]) - int(data[i]))**2
    return sum/len(data)
    
def split_channel(data):
    """
    Detect the number of channels in the data
    """
    if len(data.shape) == 1:
        return [data]
    elif data.shape[1] == 2:
        left_channel = data[:, 0]
        right_channel = data[:, 1]
        return [left_channel, right_channel]
