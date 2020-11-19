from tools import *
from numpy import pad, array, round, zeros
import math

N = 500 # number of samples
pi = math.pi

def mdct(sample_rate, data):
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
	
	for i in range(0,count):
		tmp = frame[i].dot(matrix.T) # mdct cho tung frame ma chua biet luu vao dau


# create Nx2X matrix
def gen_matrix(samples): 
	matrix = zeros(shape=(samples,samples*2))
	for k in range(0,samples):
    		for n in range(0,samples*2):
        		temp = 2*pi*(2*n+1+samples)*(2*k+1)
        		matrix[k][n] = math.cos(temp/(8*samples))
	#print(matrix)
	return matrix

original_file = "audios/human_voice.wav"
samplerate, data = read_audio_file(original_file)
print(mdct(samplerate, data)) 

