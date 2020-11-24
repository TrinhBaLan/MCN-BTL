from tools import *
from numpy import pad, array, zeros, dot, hstack
import math

N = 1000  # number of samples
pi = math.pi


def mdct_transform(sample_rate, data, file):
    print("Original data: ", data)
    print("Plotting original data...")
    plot_waveform(len(data) / sample_rate, data, "Original")
    # matrix = gen_matrix(N//2)
    # matrix to transform 2 frames at once
    matrix = gen_matrix(N)

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

    # Overlapping MDCT
    print("Performing MDCT on signal...")
    mdct = []
    for i in range(0, count-1):
        # Merge frame i with i+1 then perform MDCT
        tmp = dot(matrix, hstack((frame[i],(frame[i+1]))).T)
        mdct.append(tmp)
    #print(len(mdct))

    # Inverse MDCT and split into halfs
    frame_inv = []
    for mdct_frame in mdct:
        tmp = dot(matrix.T, mdct_frame)/(2*N)
        frame_inv.append(tmp[:N])
        frame_inv.append(tmp[N:])
    #print(len(frame_inv))

    # Resolve overlapping to reduce end-effect at the border of frames
    reconstructed_frames = []
    i = 0
    while i < len(frame_inv): 
        if (i == 0) or (i == len(frame_inv)-1):
            # The first and the last frames are not overlapped
            reconstructed_frames.append(frame_inv[i])
            i+=1
        else:
            #print(i)
            # Adding overlapped frames together
            tmp = []
            #print(len(frame_inv[i]))
            #print(len(frame_inv[i+1]))
            for j in range(0, len(frame_inv[i])):
                #print(j)
                tmp.append(frame_inv[i][j] + frame_inv[i+1][j])
            reconstructed_frames.append(tmp)
            i+=2
    
    #print(reconstructed_frames[0])

    reconstrusted_data = []
    # for imdct_frame in frame_inv:
    for imdct_frame in reconstructed_frames:
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
