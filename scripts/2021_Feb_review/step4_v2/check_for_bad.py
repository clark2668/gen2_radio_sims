import h5py
import tarfile
import argparse

parser = argparse.ArgumentParser(description='Merge hdf5 files')
parser.add_argument('files', nargs='+', help='input file or files')
args = parser.parse_args()

filenames = args.files[0:]

for f in filenames:
	# print('Working on file {}'.format(f))
	if '.tar.gz' in f:
		tar = tarfile.open(f, 'r:gz')
		for member in tar.getmembers():
			# print('member {}'.format(member))
			if member.isfile():
# 				# f_extracted = tar.extract(member)
				f_extracted = tar.extractfile(member)
				fin = h5py.File(f_extracted, 'r')
				print('{}, {}'.format(member.name, fin.attrs['n_events']))
				fin.close()


