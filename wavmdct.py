#!/usr/bin/env python3

import argparse
from tools import *
from dct import dct_transform
from mdct import mdct_transform

def main():
    # Initiate the program and add arguments to the program
    program = argparse.ArgumentParser(prog="wavmdct", description="Compress WAV audio files with MDCT")
    program.add_argument("file", help="input file location")
    program.add_argument("-d", "--dct", action="store_true", help="use DCT on the input audio file")
    program.add_argument("-m", "--mdct", action="store_true", help="use MDCT on the input audio file")
    args = program.parse_args()

    # First we detect the number of channels in the file. Then perform DCT or MDCT on each channel
    if (args.dct):
        samplerate, data = read_audio_file(args.file)
        channel_data = split_channel(data)
        transformed = []
        for channel in channel_data:
            transformed.append(dct_transform(samplerate, channel, args.file))
        reconstrusted_file = "outputs/dct/" + args.file.split("/")[-1]  # Get the filename
        print(f"Writing to {reconstrusted_file}")
        write_audio_file(reconstrusted_file, samplerate, transformed)
        print("DONE!")

    elif (args.mdct):
        samplerate, data = read_audio_file(args.file)
        channel_data = split_channel(data)
        transformed = []
        for channel in channel_data:
            transformed.append(mdct_transform(samplerate, data, args.file))
        # Write the reconstructed data to a new file in the outputs folder
        reconstrusted_file = "outputs/mdct/" + args.file.split("/")[-1] # Get the filename
        print(f"Writing to {reconstrusted_file}")
        write_audio_file(reconstrusted_file, samplerate, transformed)
        print("DONE!")

    else:
        print("No DCT or MDCT options given. Exiting...")

main()
