import numpy as np
import sys
import pickle as pickle
import os
import json
from helper import trigger_combinations
from NuRadioMC.utilities import Veff

def make_dummy(outfile, energy, czmin, czmax):
    thetamin = np.arccos(float(czmin))
    thetamax = np.arccos(float(czmax))
    energy = float(energy)

    # open the dummy file full of zeros
    f = open('dummy.json')
    data = json.load(f)
    the_data = data[0]

    # swap out the relevant keys
    the_data['thetamin'] = thetamin
    the_data['thetamax'] = thetamax
    the_data['energy'] = energy
    the_data['energy_max'] = energy
    the_data['energy_min'] = energy
        
    # write the result out
    with open(outfile, 'w') as outfile:
        json.dump([the_data], outfile, sort_keys=True, indent=4)


if __name__ == "__main__":

    infile = sys.argv[1]
    outfile = sys.argv[2]
    logenergy = float(sys.argv[3])
    energy = 10 ** logenergy
    czmin = float(sys.argv[4])
    czmax = float(sys.argv[5])

    if not os.path.exists(infile):
        print("input file does not exist {}. Need to make a dummy file!".format(infile))
        make_dummy(outfile, energy, czmin, czmax)
        sys.exit()
    
    try:
        v = Veff.get_Veff_Aeff(infile, trigger_combinations=trigger_combinations)
        Veff.export(outfile, v, export_format="json")
    except:
        print("our attempt at actually making the file failed. Make a dummy.")
        make_dummy(outfile, energy, czmin, czmax)

