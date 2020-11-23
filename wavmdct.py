#!/usr/bin/env python3
import argparse
from tools import *
from dct import dct_transform
from mdct import mdct_transform

def main():
    program = argparse.ArgumentParser(prog="wavmdct", description="Compress WAV audio files with MDCT")
    program.add_argument("file", help="input file location")
    program.add_argument("-d", "--dct", action="store_true", help="use DCT on the input audio file")
    program.add_argument("-m", "--mdct", action="store_true", help="use MDCT on the input audio file")
    args = program.parse_args()
    if (args.dct):
        samplerate, data = read_audio_file(args.file)
        dct_transform(samplerate, data, args.file)
    elif (args.mdct):
        samplerate, data = read_audio_file(args.file)
        mdct_transform(samplerate, data, args.file)
    else:
        print("No DCT or MDCT options given. Exiting...")

main()
