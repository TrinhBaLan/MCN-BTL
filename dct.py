from scipy.fft import dct, idct
from tools import *
from numpy import pad, array, round
from CompressedFile import *

def dct_transform(sample_rate, data, file, sample_per_frame, compress_ratio):
    print("Original data: ", data)

    # Pad zeroes to the end of the data array so that the number of array elements is divisible to {sample}
    numzeros = sample_per_frame - len(data) % sample_per_frame # Number of zeroes to be padded
    print("Padding zeroes to original data...")
    padded_data = pad(data, (0, numzeros), "constant", constant_values=0)

    # Divide the data into frames of {sample} each
    frames = {}
    count = 0
    print(f"Dividing data into {sample_per_frame} frames...")
    for i in range(0, len(padded_data), sample_per_frame):
        frames[count] = padded_data[i:i+sample_per_frame]
        count += 1

    # Perform DCT on each frame, slice the frame to the data cutoff index, pad zeroes and use IDCT
    frames_idct = {}
    compressed_data = []
    sample_taken = int(round(sample_per_frame * compress_ratio))

    print("Performing DCT on each frame...")
    for num in frames:
        dct_frame = dct(frames[num], norm="ortho")[:sample_taken]
        compressed_data.append(dct_frame.astype(data.dtype))
        padded_dct_frame = pad(dct_frame, (0, sample_per_frame - sample_taken), "constant", constant_values=0)
        frames_idct[num] = idct(padded_dct_frame, norm="ortho")

    # Write the compressed data to a new binary file with extension cpz
    print("Writing to a compressed file in './compressed/dct/' ...")
    filename = file.split("/")[1] # Get the filename
    compressed = CompressedFile(Type.DCT, compressed_data)
    write_compressed_file(compressed, "dct/" + filename.split(".")[0] + ".cpz")

    # Reconstruct the data array from frames
    reconstrusted_data = []
    for num in frames_idct:
        reconstrusted_data.extend(frames_idct[num])
    reconstrusted_data = array(reconstrusted_data)[:len(data)].astype(data.dtype)

    return reconstrusted_data
