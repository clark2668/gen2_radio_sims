import os
import sys
import numpy as np
import h5py
import argparse

parser = argparse.ArgumentParser(description='Merge hdf5')
parser.add_argument('files', nargs='+', help='input files')
args = parser.parse_args()
input_files = args.files[1:]
for f in input_files:
	print(f)
	fin = h5py.File(f, 'r')
	fin.close()