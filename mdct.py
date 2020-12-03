from tools import *
from numpy import pad, array, zeros, dot, hstack
import math
from CompressedFile import CompressedFile

pi = math.pi

def mdct_transform(sample_rate, data, file, sample_per_frame, compress_ratio):
    print("Original data: ", data)
    #print("Plotting original data...")
    #plot_waveform(len(data) / sample_rate, data, "Original")
    # matrix = gen_matrix(sample_per_frame//2)
    # matrix to transform 2 frames at once
    matrix = gen_matrix(sample_per_frame)

    # Pad zeroes so the data can be divided by sample_per_frame
    print("Padding zeroes to original data...")
    numzeros = sample_per_frame - len(data) % sample_per_frame
    padded_data = pad(data, (0, numzeros), "constant", constant_values=0)

    # Divide data to frames
    print(f"Dividing data to {sample_per_frame} frame...")
    frame = {}
    count = 0
    for i in range(0, len(padded_data), sample_per_frame):
        frame[count] = padded_data[i:i+sample_per_frame]
        count += 1
    # print(frame)

    # Overlapping MDCT
    print("Performing MDCT on signal...")
    mdct = []
    for i in range(0, count-1):
        # Merge frame i with i+1 then perform MDCT
        tmp = dot(matrix, hstack((frame[i],(frame[i+1]))).T)
        mdct.append(tmp)
    samples_keep = int(round(sample_per_frame*compress_ratio))

    compressed_mdct = []
    for i in range(0, len(mdct)):
        compressed_mdct.append(mdct[i][:samples_keep])

    compressed_data = []
    for frame in compressed_mdct:
        compressed_data.append(frame.astype(data.dtype))
    # Write the compressed data to a new binary file with extension cpz
    print("Writing to a compressed file in './compressed/mdct/' ...")
    filename = file.split("/")[1] # Get the filename
    compressed = CompressedFile("MDCT", compressed_data)
    write_compressed_file(compressed, "mdct/" + filename.split(".")[0] + ".cpz")

    # Inverse MDCT and split into halfs
    frame_inv = []
    for mdct_frame in compressed_mdct:
        # Pad zeroes to frame to restore size
        mdct_frame = pad(mdct_frame, (0, (sample_per_frame - samples_keep)), "constant", constant_values=0)
        tmp = dot(matrix.T, mdct_frame)/sample_per_frame
        frame_inv.append(tmp[:sample_per_frame])
        frame_inv.append(tmp[sample_per_frame:])
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
    
    reconstrusted_data = []
    # for imdct_frame in frame_inv:
    for imdct_frame in reconstructed_frames:
        reconstrusted_data.extend(imdct_frame)

    reconstrusted_data = array(reconstrusted_data)[:len(data)].astype(data.dtype)

    return reconstrusted_data

# Create Nx2N matrix
def gen_matrix(samples):
    matrix = zeros(shape=(samples, samples * 2))
    for k in range(0, samples):
        for n in range(0, samples * 2):
            temp = 2 * pi * (2 * n + 1 + samples) * (2 * k + 1)
            matrix[k][n] = math.cos(temp / (8 * samples))
    return matrix
