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

def write_audio_file(path, samplerate, data):
    """
    Write spectified audio data to a WAV file
    :param path: File location
    :param samplerate: Sample rate of the data
    :param data: Audio data as numpy array
    """
    try:
        write(path, samplerate, data)
    except WavFileWarning:
        print("There seems to be a problem reading your WAV file.")

def plot_waveform(length, data, data_label):
    """
    Plot the specified data
    :param length: Length of the audio file
    :param data: Audio data as numpy array
    """
    time = np.linspace(0., length, data.shape[0])
    plt.plot(time, data, label=data_label)
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.savefig("test.png")
