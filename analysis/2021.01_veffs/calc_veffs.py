import numpy as np
import sys
import pickle as pickle

from NuRadioMC.utilities.Veff import get_Veff_Aeff, get_Veff_Aeff_array

top_dir = '/data/user/brianclark/Gen2/simulation_output/secondaries_500km2/step3/surface_4LPDA_PA_15m_RNOG_300K_1.50km/config_Alv2009_noise_100ns/D09surface_4LPDA_pa_15m_250MHz/e'

data = get_Veff_Aeff(top_dir, n_cores=4)
output = open('thefile.pkl', 'wb')
pickle.dump(data, output)

