from scipy.fft import dct, idct
from tools import *
from numpy import pad, array, round
from numpy.linalg import norm

sample = 500 # Number of samples
compress_ratio = 0.2 # Compressed data size to original data size

def dct_transform():
    original_file = "audios/human_voice.wav"
    samplerate, data = read_audio_file(original_file)

    print("Original data: ", data)
    print("Plotting original data to test.png...")
    plot_waveform(len(data)/samplerate, data, "Original")

    numzeros = sample - len(data) % sample # Number of zeroes to be padded 
    print("Padding zeroes to original data...")
    padded_data = pad(data, (0, numzeros), "constant", constant_values=0) # Pad zeroes to the end of the data array so that the number of array elements is divisible to {sample}

    # Divide the data into frames of {sample} each
    frames = {}
    count = 0
    print(f"Dividing data into {sample} frames...")
    for i in range(0, len(padded_data), sample):
        frames[count] = padded_data[i:i+sample]
        count += 1

    # Perform DCT on each frame, specify the index of data cutoff, pad zeroes and use IDCT
    frames_idct = {}
    sample_taken = int(round(sample * compress_ratio))

    print("Performing DCT on each frame...")
    for num in frames:
        dct_frame = dct(frames[num])[:sample_taken]
        padded_dct_frame = pad(dct_frame, (0, sample - sample_taken), "constant", constant_values=0)
        frames_idct[num] = idct(padded_dct_frame)

    # Reconstruct the data array from frames
    reconstrusted_data = []
    for num in frames_idct:
        reconstrusted_data.extend(frames_idct[num])
    
    reconstrusted_data = array(reconstrusted_data)[:len(data)].astype(data.dtype)
    #print(str(reconstrusted_data.dtype))
    

    print("Writing to a new audio file...")
    reconstrusted_file = "outputs/" + original_file.split("/")[1].split(".")[0] + "-dct.wav" # Get the filename before the extension
    write_audio_file(reconstrusted_file, samplerate, reconstrusted_data)

    print("Plotting reconstructed data to test.png...")
    plot_waveform(len(reconstrusted_data) / samplerate, reconstrusted_data, "Reconstructed")
    print("DONE!")

    print("MSE: " + str(mse_eval(data, reconstrusted_data)))
dct_transform()


