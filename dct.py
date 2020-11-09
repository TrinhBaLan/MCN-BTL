from scipy.fft import dct, idct
from tools import read_audio_file, write_audio_file

def transform():
    file = "audios/human_voice.wav"
    samplerate, data = read_audio_file(file)
    newdata = idct(dct(data))
    newfile = "audios/" + file.split("/")[1].split(".")[0] + "-dct.wav" # Get the filename, then change it to filename-dct
    print("Sample rate: ", samplerate)
    write_audio_file(newfile, samplerate, newdata) # Does not work

transform()