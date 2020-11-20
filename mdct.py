from tools import *
from numpy import pad, array, round, zeros
import math

N = 500 # number of samples
pi = math.pi

def mdct(sample_rate, data):
	plot_waveform(len(data)/sample_rate, data, "Original")
	matrix = gen_matrix(N)
	numzeros = N - len(data) % N
	padded_data = pad(data, (0, numzeros), "constant", constant_values=0)
	
	print(data.shape)
	print(padded_data.shape)
	print(padded_data)
	# divide data to frames
	frame = {}
	count = 0
	for i in range(0,len(padded_data)-N,N):
    		frame[count] = array([padded_data[i:i+N*2]])
    		count+=1
	#print(frame)
	
	mdct = []
	for i in range(0,count):
    		tmp = matrix.dot(frame[i].T)
    		mdct.extend(tmp.flatten())


	frame_inv = {}
	count_inv = 0
	for i in range(0,len(mdct),N):
    		frame_inv[count_inv] = array([mdct[i:i+N]])
    		count_inv +=1
	
	reconstrusted_data = []
	for i in range(0,count_inv):
    		tmp = (matrix.T).dot(frame_inv[i].T)
    		reconstrusted_data.extend(tmp.flatten())
	reconstrusted_data = array(reconstrusted_data)[:len(data)].astype(data.dtype)
	print(reconstrusted_data)
	reconstrusted_file = "outputs/" + original_file.split("/")[1].split(".")[0] + "-dct.wav" # Get the filename before the extension
	write_audio_file(reconstrusted_file, sample_rate, reconstrusted_data)
	#plot_waveform(len(reconstrusted_data) / sample_rate, reconstrusted_data, "Reconstructed")

# create Nx2X matrix
def gen_matrix(samples): 
	matrix = zeros(shape=(samples,samples*2))
	for k in range(0,samples):
    		for n in range(0,samples*2):
        		temp = 2*pi*(2*n+1+samples)*(2*k+1)
        		matrix[k][n] = math.cos(temp/(8*samples))
	#print(matrix)
	return matrix

original_file = "audios/laser.wav"
samplerate, data = read_audio_file(original_file)
print(mdct(samplerate, data)) 

