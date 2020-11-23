from tools import *
from numpy import pad, array, zeros, dot
import math

N = 1000  # number of samples
pi = math.pi


def mdct_transform(sample_rate, data, file):
    print("Original data: ", data)
    print("Plotting original data...")
    plot_waveform(len(data) / sample_rate, data, "Original")
    matrix = gen_matrix(N//2)

    print("Padding zeroes to original data...")
    numzeros = N - len(data) % N
    padded_data = pad(data, (0, numzeros), "constant", constant_values=0)

    # divide data to frames
    print(f"Dividing data to {N} frame...")
    frame = {}
    count = 0
    for i in range(0, len(padded_data), N):
        frame[count] = padded_data[i:i+N]
        count += 1
    # print(frame)

    print("Performing MDCT on each frame...")
    mdct = []
    for i in range(0, count):
        tmp = dot(matrix, frame[i].T)
        mdct.append(tmp)
#    print(mdct)

    frame_inv = []
    for mdct_frame in mdct:
        tmp = dot(matrix.T, mdct_frame)/N
        frame_inv.append(tmp)

    reconstrusted_data = []
    for imdct_frame in frame_inv:
        reconstrusted_data.extend(imdct_frame)

    reconstrusted_data = array(reconstrusted_data)[:len(data)].astype(data.dtype)

    reconstrusted_file = "outputs/mdct/" + file.split("/")[-1]  # Get the filename
    print(f"Writing to outputs/mdct/{reconstrusted_file}")
    write_audio_file(reconstrusted_file, sample_rate, reconstrusted_data)

    print("Plotting reconstructed data...")
    plot_waveform(len(reconstrusted_data) / sample_rate, reconstrusted_data, "Reconstructed")
    print("DONE!")

# create Nx2X matrix
def gen_matrix(samples):
    matrix = zeros(shape=(samples, samples * 2))
    for k in range(0, samples):
        for n in range(0, samples * 2):
            temp = 2 * pi * (2 * n + 1 + samples) * (2 * k + 1)
            matrix[k][n] = math.cos(temp / (8 * samples))
    return matrix
