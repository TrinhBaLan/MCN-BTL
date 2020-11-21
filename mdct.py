from tools import *
from numpy import pad, array, zeros, dot
import math

N = 500  # number of samples
pi = math.pi


def mdct(sample_rate, data):
    plot_waveform(len(data) / sample_rate, data, "Original")
    matrix = gen_matrix(N)
    numzeros = N - len(data) % N
    padded_data = pad(data, (0, numzeros), "constant", constant_values=0)
    print(data)

    # divide data to frames
    frame = {}
    count = 0
    for i in range(0, len(padded_data) - N, N):
        frame[count] = padded_data[i:i+N*2]
        count += 1
    # print(frame)

    mdct = []
    for i in range(0, count):
        tmp = dot(matrix, frame[i].T)
        mdct.append(tmp)
#    print(mdct)

    frame_inv = []
    for mdct_frame in mdct:
        tmp = dot(matrix.T, mdct_frame.T)/N
        frame_inv.append(tmp)

    reconstrusted_data = []
    for imdct_frame in frame_inv:
        reconstrusted_data.extend(array(imdct_frame).flatten())

    reconstrusted_data = array(reconstrusted_data)[:len(data)].astype(data.dtype)
    print(reconstrusted_data)
    reconstrusted_file = "outputs/" + original_file.split("/")[1].split(".")[0] + "-mdct.wav"  # Get the filename before the extension
    write_audio_file(reconstrusted_file, sample_rate, reconstrusted_data)
    plot_waveform(len(reconstrusted_data) / sample_rate, reconstrusted_data, "Reconstructed")

# create Nx2X matrix
def gen_matrix(samples):
    matrix = zeros(shape=(samples, samples * 2))
    for k in range(0, samples):
        for n in range(0, samples * 2):
            temp = 2 * pi * (2 * n + 1 + samples) * (2 * k + 1)
            matrix[k][n] = math.cos(temp / (8 * samples))
    return matrix


original_file = "audios/human_voice.wav"
samplerate, data = read_audio_file(original_file)
print(mdct(samplerate, data))
