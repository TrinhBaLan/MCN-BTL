from scipy.fft import dct, idct
from tools import *
from numpy import pad, array, round

sample = 500 # Number of samples
compress_ratio = 0.5 # Compressed data size to original data size

def dct_transform(sample_rate, data, file):
    print("Original data: ", data)
    print("Plotting original data to graph.png...")
    plot_waveform(len(data)/sample_rate, data, "Original")

    # Pad zeroes to the end of the data array so that the number of array elements is divisible to {sample}
    numzeros = sample - len(data) % sample # Number of zeroes to be padded 
    print("Padding zeroes to original data...")
    padded_data = pad(data, (0, numzeros), "constant", constant_values=0) 
    # Divide the data into frames of {sample} each
    frames = {}
    count = 0
    print(f"Dividing data into {sample} frames...")
    for i in range(0, len(padded_data), sample):
        frames[count] = padded_data[i:i+sample]
        count += 1

    # Perform DCT on each frame, slice the frame to the data cutoff index, pad zeroes and use IDCT
    frames_idct = {}
    sample_taken = int(round(sample * compress_ratio))

    print("Performing DCT on each frame...")
    for num in frames:
        dct_frame = dct(frames[num], norm="ortho")[:sample_taken]
        padded_dct_frame = pad(dct_frame, (0, sample - sample_taken), "constant", constant_values=0)
        frames_idct[num] = idct(padded_dct_frame, norm="ortho")

    # Reconstruct the data array from frames
    reconstrusted_data = []
    for num in frames_idct:
        reconstrusted_data.extend(frames_idct[num])
    reconstrusted_data = array(reconstrusted_data)[:len(data)].astype(data.dtype)
    # Plot the reconstructed data
    print("Plotting reconstructed data to graph.png...")
    plot_waveform(len(reconstrusted_data) / sample_rate, reconstrusted_data, "Reconstructed")
    return reconstrusted_data
