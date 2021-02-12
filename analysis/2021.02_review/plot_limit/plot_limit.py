import numpy as np
import matplotlib.pyplot as plt
from NuRadioMC.examples.Sensitivities import E2_fluxes3 as limits
from NuRadioMC.utilities import fluxes
from NuRadioReco.utilities import units


n_deep = 144
n_shallow = (169+144)
livetime = 10 * units.year
uptime = 1.

data = np.genfromtxt('tabulated_veff_aeff.csv', delimiter=',', skip_header=1, names=['logE', 'dveff', 'daff', 'sveff', 'saeff'])
energies = np.power(10.,data['logE'])


fig, ax = limits.get_E2_limit_figure(show_ice_cube_EHE_limit=True,
										show_ice_cube_HESE_data=False,
										show_ice_cube_HESE_fit=False,
										show_ice_cube_mu=True,
										show_anita_I_III_limit=False,
										show_auger_limit=True,
										diffuse=True, show_grand_10k=False, show_grand_200k=False, show_Heinze=True, show_TA=True,
										show_ara=False, show_arianna=False, show_IceCubeGen2=False, shower_Auger=False)

limit_deep = fluxes.get_limit_e2_flux(energy=energies[1:]*units.eV, veff_sr= n_deep * data['dveff'][1:]*units.km**3*units.sr, livetime=livetime*uptime)
limit_shallow = fluxes.get_limit_e2_flux(energy=energies[1:]*units.eV, veff_sr= n_shallow * data['sveff'][1:]*units.km**3*units.sr, livetime=livetime*uptime)
limit_combo = fluxes.get_limit_e2_flux(energy=energies[1:]*units.eV, veff_sr= (n_shallow * data['sveff'][1:]*units.km**3*units.sr) + (n_deep * data['dveff'][1:]*units.km**3*units.sr), livetime=livetime*uptime)

ax.plot(np.power(10.,data['logE'][1:])/limits.plotUnitsEnergy, limit_shallow/limits.plotUnitsFlux, 'C1--', label='Shallow Only ({} sta, {} yrs, {}% uptime)'.format(n_shallow , livetime/units.year, uptime*100))
ax.plot(np.power(10.,data['logE'][1:])/limits.plotUnitsEnergy, limit_deep/limits.plotUnitsFlux, 'C0--', label='Deep Only ({} sta, {} yrs, {}% uptime)'.format(n_deep , livetime/units.year, uptime*100))
ax.plot(np.power(10.,data['logE'][1:])/limits.plotUnitsEnergy, limit_combo/limits.plotUnitsFlux, 'C2--', label='Combo ({} deep, {} shallow, {} yrs, {}% uptime)'.format(n_deep, n_shallow , livetime/units.year, uptime*100))
ax.legend()
ax.set_title('Trigger Level')
fig.savefig('limit_v2.png')