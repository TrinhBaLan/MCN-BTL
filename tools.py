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
            output = np.vstack((left_channel, right_channel)).T
            write(path, samplerate, output)

    except WavFileWarning:
        print("There seems to be a problem reading your WAV file.")

def plot_waveform(samplerate, original_data, transformed_data, number_of_channels):
    """
    Plot the specified data
    :param samplerate: Sample rate of the audio file
    :param data: Audio data as numpy array
    """
    length = len(original_data[0])/samplerate
    time = np.linspace(0., length, original_data[0].shape[0])
    fig, ax = plt.subplots(number_of_channels)
    axs = []
    if number_of_channels == 1:
        axs.append(ax)
    elif number_of_channels == 2:
        axs.extend(ax)
    fig.suptitle("Graph of audio signal")
    #plt.setp(axs[:], xlabel='Time')
    #plt.setp(axs[:], ylabel='Amplitude')
    for i in range(0, number_of_channels):
        axs[i].plot(time, original_data[i], label='Original', linewidth=1,zorder=1)
        axs[i].plot(time, transformed_data[i], label='Reconstructed', linewidth=1, zorder=2)
        axs[i].legend(loc="upper right")
        '''
        if i == 0:
            axs[i].set_title('Left Channel')
        elif i == 1:
            axs[i].set_title('Right Channel')
        '''
    plt.savefig("graph.png")           

    '''
    time = np.linspace(0., length, data.shape[0])
    plt.title("Graph of audio signal")
    plt.plot(time, data, label=data_label)
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.savefig("graph.png")
    '''

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
