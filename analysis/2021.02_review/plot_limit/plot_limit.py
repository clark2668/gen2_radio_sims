import numpy as np
import matplotlib.pyplot as plt
from NuRadioMC.examples.Sensitivities import E2_fluxes3 as limits
from NuRadioMC.utilities import fluxes
from NuRadioReco.utilities import units
from NuRadioMC.utilities import cross_sections


n_deep = 144
n_shallow = (169+144)
livetime = 10 * units.year
uptime = 0.9

data = np.genfromtxt('tabulated_veff_aeff_review_hybrid.csv', delimiter=',', skip_header=6, names=['logE', 'dveff', 'daff', 'sveff', 'saeff', 'o', 'do', 'so', 'alat'])
energies = np.power(10.,data['logE'])
# optical_data = np.genfromtxt('gen2_optical_aeff.csv', delimiter=',', skip_header=1, names=['logE', 'aeff'])
# optical_energies = np.power(10.,optical_data['logE'])*units.eV
# optical_aeffs = optical_data['aeff']*units.km**2
# optical_veffs = optical_aeffs * cross_sections.get_interaction_length(optical_energies)*4*np.pi

# icecube_data = np.genfromtxt('IceCube_aeff.csv', delimiter=',', skip_header=1, names=['E', 'aeff'])
# icecube_energies = icecube_data['E']*units.GeV
# icecube_aeffs = icecube_data['aeff']*units.m**2 * units.sr
# icecube_veffs = icecube_aeffs * cross_sections.get_interaction_length(icecube_energies)

# icecube_data_prl = np.genfromtxt('IceCube_Exposure.csv', delimiter=',', skip_header=1, names=['GeV', 'Exposure'])
# icecube_prl_energies = icecube_data_prl['GeV'] * units.GeV
# icecube_prl_exposure = icecube_data_prl['Exposure'] /3 * units.second * units.sr * units.cm * units.cm
# icecube_prl_aeff_sr = icecube_prl_exposure/(2426 * units.day)
# icecube_prl_veff_sr = icecube_prl_aeff_sr * cross_sections.get_interaction_length(icecube_prl_energies)

# output_csv = 'log10(E) [eV], veff [km^3 sr], aeff [km^2 sr]'
# output_csv += "\n"
# for i, e in enumerate(icecube_prl_energies):
# 	output_csv+="{:.2f}, {:e}, {:e}\n".format(np.log10(icecube_prl_energies[i]/units.eV), 5*icecube_prl_veff_sr[i]/units.km**3, 5*icecube_prl_aeff_sr[i]/units.km**2)

# with open('scaled_icecube_prl_veff.csv', 'w') as f:
# 	f.write(output_csv)

fig, ax = limits.get_E2_limit_figure(show_ice_cube_EHE_limit=True,
										show_ice_cube_HESE_data=False,
										show_ice_cube_HESE_fit=False,
										show_ice_cube_mu=True,
										show_anita_I_III_limit=True,
										show_auger_limit=False,
										diffuse=True, show_grand_10k=False, show_grand_200k=False, show_Heinze=False, show_TA=False,
										show_ara=False, show_arianna=False, show_IceCubeGen2=False, shower_Auger=False)

# limit_deep = fluxes.get_limit_e2_flux(energy=energies[1:]*units.eV, veff_sr= n_deep * data['dveff'][1:]*units.km**3*units.sr, livetime=livetime*uptime)
# limit_shallow = fluxes.get_limit_e2_flux(energy=energies[1:]*units.eV, veff_sr= n_shallow * data['sveff'][1:]*units.km**3*units.sr, livetime=livetime*uptime)
limit_combo = fluxes.get_limit_e2_flux(energy=energies*units.eV, veff_sr= ((n_shallow * data['sveff']*units.km**3*units.sr) + (n_deep * data['dveff']*units.km**3*units.sr))*(1/(1+data['o'])), livetime=livetime*uptime, upperLimOnEvents=1)
# limit_gen2 = fluxes.get_limit_e2_flux(energy=optical_energies, veff_sr= optical_veffs, livetime=livetime*uptime)
# limit_i3 = fluxes.get_limit_e2_flux(energy=icecube_energies, veff_sr= icecube_veffs/5, livetime=livetime*uptime)
# limit_i3_prl = fluxes.get_limit_e2_flux(energy=icecube_prl_energies, veff_sr= icecube_prl_veff_sr, livetime=10*units.year)
# limit_i3_prl_div3 = fluxes.get_limit_e2_flux(energy=icecube_prl_energies, veff_sr= icecube_prl_veff_sr/3, livetime=10*units.year)

for i,j in zip(energies, limit_combo):
	print('{:e}, {:e}'.format(i/limits.plotUnitsEnergy, j/limits.plotUnitsFlux))


# ax.plot(np.power(10.,data['logE'][1:])/limits.plotUnitsEnergy, limit_shallow/limits.plotUnitsFlux, 'C1--', label='Shallow Only ({} sta, {} yrs, {}% uptime)'.format(n_shallow , livetime/units.year, uptime*100))
# ax.plot(np.power(10.,data['logE'][1:])/limits.plotUnitsEnergy, limit_deep/limits.plotUnitsFlux, 'C0--', label='Deep Only ({} sta, {} yrs, {}% uptime)'.format(n_deep , livetime/units.year, uptime*100))
ax.plot(np.power(10.,data['logE'])/limits.plotUnitsEnergy, limit_combo/limits.plotUnitsFlux, 'C2--', label='Combo ({} deep, {} shallow, {} yrs, {}% uptime)'.format(n_deep, n_shallow , livetime/units.year, uptime*100))
# ax.plot(optical_energies/limits.plotUnitsEnergy, limit_gen2/limits.plotUnitsFlux, 'C3-.', label='Gen2-Optical')
# ax.plot(icecube_energies/limits.plotUnitsEnergy, limit_i3/limits.plotUnitsFlux, 'C4:', label='IceCube')
# ax.plot(icecube_prl_energies/limits.plotUnitsEnergy, limit_i3_prl/limits.plotUnitsFlux, 'C4:', label='Scale by 10 years')
# ax.plot(icecube_prl_energies/limits.plotUnitsEnergy, limit_i3_prl_div3/limits.plotUnitsFlux, 'C3-.', label='Scale by 10 years/3')
# ax.set_xlim([1e11,1e20])
ax.legend()
ax.set_title('Trigger Level')
fig.savefig('limit_v2.png')