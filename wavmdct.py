#!/usr/bin/env python3

import argparse
from tools import *
from dct import dct_transform
from mdct import mdct_transform
from pathlib import Path

def main():
    # Initiate the program and add arguments to the program
    program = argparse.ArgumentParser(prog="wavmdct", description="Compress WAV audio files with MDCT")
    program.add_argument("file", help="input file location")
    program.add_argument("-d", "--dct", action="store_true", help="use DCT on the input audio file")
    program.add_argument("-m", "--mdct", action="store_true", help="use MDCT on the input audio file")
    args = program.parse_args()

    # First we detect the number of channels in the file. Then perform DCT or MDCT on each channel
    if (args.dct):
        handle_dct(args.file)
    elif (args.mdct):
        handle_mdct(args.file)
    else:
        print("No DCT or MDCT options given. Exiting...")

def handle_dct(file):
    """
    Handle the DCT options
    """
    samplerate, data = read_audio_file(file)
    channel_data = split_channel(data)
    transformed = []
    for channel in channel_data:
        transformed.append(dct_transform(samplerate, channel, file))
    # Plot original and reconstructed waveform
    plot_waveform(samplerate, channel_data, transformed, len(channel_data))
    # Check if output folder exists, create it if it isn't
    if not Path("./outputs/dct/").is_dir():
        Path("./outputs/dct/").mkdir(parents=True)

    # Write the reconstructed data to a new file in the outputs folder
    reconstrusted_file = "./outputs/dct/" + file.split("/")[-1]  # Get the filename
    print(f"Writing to '{reconstrusted_file}'")
    write_audio_file(reconstrusted_file, samplerate, transformed)
    print("DONE!")


def handle_mdct(file):
    """
    Handle the MDCT option
    """
    samplerate, data = read_audio_file(file)
    channel_data = split_channel(data)
    transformed = []
    for channel in channel_data:
        transformed.append(mdct_transform(samplerate, channel, file))
    # Plot original and reconstructed waveform
    plot_waveform(samplerate, channel_data, transformed, len(channel_data))
    # Check if output folder exists, create it if it isn't
    if not Path("./outputs/mdct/").is_dir():
        Path("./outputs/mdct/").mkdir(parents=True)

    # Write the reconstructed data to a new file in the outputs folder
    reconstrusted_file = "./outputs/mdct/" + file.split("/")[-1]  # Get the filename
    print(f"Writing to '{reconstrusted_file}'")
    write_audio_file(reconstrusted_file, samplerate, transformed)
    print("DONE!")


main()
