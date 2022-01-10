import numpy as np
import sys
import pickle as pickle

from Veff import get_Veff_Aeff, get_Veff_Aeff_array, get_index, get_Veff_water_equivalent

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

        data = get_Veff_Aeff(topdir+'/', n_cores=4)
        # Veffs, energies, energies_low, energies_up, zenith_bins, utrigger_names = get_Veff_Aeff_array(data)
        # Veff = np.average(Veffs[:, :, get_index("all_triggers", utrigger_names), 0], axis=1)
        # Veff = get_Veff_water_equivalent(Veff) * 4 * np.pi
        # # calculate the uncertainty for the average over all zenith angle bins. The error relative error is just 1./sqrt(N)
        # Veff_error = Veff / np.sum(Veffs[:, :, get_index("all_triggers", utrigger_names), 2], axis=1) ** 0.5

        # the_outputs = {}
        # the_outputs['veff'] = Veff
        # the_outputs['veff_err'] = Veff_error

        filename = f'DETECTOR_{detfile}_____CONFIG_{configfile}_____SIM_{simfile}_____FLAVOR_{flavor}.pkl'
        output_file = open(filename, 'wb')

        pickle.dump(data, output_file)
