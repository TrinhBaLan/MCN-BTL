#!/usr/bin/env python3

import argparse
from tools import *
from dct import dct_transform
from mdct import mdct_transform
from pathlib import Path

def main():
    # Initiate the program and add arguments to the program
    program = argparse.ArgumentParser(prog="wavmdct.py", description="Compress WAV audio files with MDCT")

    # DCT and MDCT options are mutually exclusive
    group = program.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--dct", action="store_true", help="use DCT on the input audio file")
    group.add_argument("-m", "--mdct", action="store_true", help="use MDCT on the input audio file")

    # Other required options
    program.add_argument("file", help="input file location")
    program.add_argument("-s", "--sample-per-frame", action="store", type=int, required=True, help="number of samples per frame")
    program.add_argument("-c", "--compress-ratio", action="store", type=float, required=True, help="compress ratio")
    args = program.parse_args()

    # Handle the options from the command line
    if args.dct:
        handle_dct(args.file, args.sample_per_frame, args.compress_ratio)
    elif args.mdct:
        handle_mdct(args.file, args.sample_per_frame, args.compress_ratio)
    else:
        print("No options given.")
        print("Run the program with the -h flag for help.")


def handle_dct(file, sample_per_frame, compress_ratio):
    """
    Handle the DCT options
    """
    samplerate, data = read_audio_file(file)

    # First we detect the number of channels, then perform the transform on each channel
    channel_data = split_channel(data)
    transformed = []
    for channel in channel_data:
        transformed.append(dct_transform(samplerate, channel, file, sample_per_frame, compress_ratio))

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


def handle_mdct(file, sample_per_frame, compress_ratio):
    """
    Handle the MDCT option
    """
    samplerate, data = read_audio_file(file)

    # First we detect the number of channels, then perform the transform on each channel
    channel_data = split_channel(data)
    transformed = []
    for channel in channel_data:
        transformed.append(mdct_transform(samplerate, channel, file, sample_per_frame, compress_ratio))

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
