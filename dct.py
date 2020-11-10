from scipy.fft import dct, idct
from tools import read_audio_file, write_audio_file, plot_waveform
from numpy import pad, array, round

sample = 500 # Number of samples

def dct_transform():
    original_file = "audios/human_voice.wav"
    samplerate, data = read_audio_file(original_file)

    print("Original data: ", data)
    print("Plotting original data to test.png...")
    plot_waveform(len(data)/samplerate, data, "Original")

    numzeros = sample - len(data) % sample # Number of zeroes to be padded 
    print("Padding zeroes to original data...")
    padded_data = pad(data, (0, numzeros), "constant", constant_values=0) # Pad zeroes to the end of the data array so that 

    # Divide the data into frames of {sample} each
    frames = {}
    count = 0
    print("Dividing data into frames...")
    for i in range(0, len(padded_data), sample):
        frames[count] = padded_data[i:i+sample]
        count += 1

    # Perform DCT on each frame, then take first 20 samples, pad zeroes and use IDCT
    frames_idct = {}
    sample_taken = 300

    print("Performing DCT on each frame...")
    for num in frames:
        dct_frame = dct(frames[num])[:sample_taken]
        padded_dct_frame = pad(dct_frame, (0, sample - sample_taken), "constant", constant_values=0)
        frames_idct[num] = idct(padded_dct_frame)

    reconstrusted_data = []
    for num in frames_idct:
        reconstrusted_data.extend(frames_idct[num])
    
    reconstrusted_data = array(reconstrusted_data)
    print("Reconstructed data: ", reconstrusted_data)
    print("Writing to a new audio file...")
    write_audio_file("outputs/human_voice-dct.wav", samplerate, reconstrusted_data)

    print("Plotting reconstructed data to reconstructed.png...")
    plot_waveform(len(reconstrusted_data) / samplerate, reconstrusted_data, "Reconstructed")
    print("DONE!")

dct_transform()


