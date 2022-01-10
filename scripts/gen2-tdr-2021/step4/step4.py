import numpy as np
import sys
import pickle as pickle

#from NuRadioMC.utilities.Veff import get_Veff_Aeff, get_Veff_Aeff_array
from Veff import get_Veff_Aeff

if __name__ == "__main__":

	depth = ''
	if(len(sys.argv) != 6):
		print("some arguments must be missing!")
		sys.exit()
	else:
		# ingest stuff we'll need to make the filename
		topdir = sys.argv[1]
		flavor = sys.argv[2]
		detfile = sys.argv[3]
		configfile = sys.argv[4]
		simfile = sys.argv[5]

		filename = f'DETECTOR_{detfile}_____CONFIG_{configfile}_____SIM_{simfile}_____FLAVOR_{flavor}.pkl'

		data = get_Veff_Aeff(topdir+'/', n_cores=4)
		output = open(filename, 'wb')
		pickle.dump(data, output)
