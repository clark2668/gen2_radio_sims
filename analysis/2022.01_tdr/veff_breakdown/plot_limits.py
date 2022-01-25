import numpy as np
import matplotlib.pyplot as plt
from NuRadioMC.examples.Sensitivities import E2_fluxes3 as limits
from NuRadioMC.utilities import fluxes
from NuRadioReco.utilities import units
from NuRadioMC.utilities import cross_sections

livetime = 10 * units.year
uptime = 0.9

detectors = [
    "baseline_array",
    "hex_hybrid_only_array",
    "hex_shallow_array",
    "hex_shallowheavy_array",
    "review_array"
]

config = "config_ARZ2020_noise"
detsim = "D01detector_sim"
deep_trigger = 'PA_4channel_100Hz'
shallow_trigger = 'LPDA_2of4_100Hz'

fig, ax = limits.get_E2_limit_figure(show_ice_cube_EHE_limit=True,
										show_ice_cube_HESE_data=False,
										show_ice_cube_HESE_fit=False,
										show_ice_cube_mu=True,
										show_anita_I_IV_limit=True,
										show_auger_limit=False,
										diffuse=True, show_grand_10k=False, 
                                        show_grand_200k=False, show_Heinze=False, show_TA=False,
										show_ara=False, show_arianna=False, shower_Auger=False)

detector = detectors[0]
data_baseline = np.genfromtxt(f'results/veff_{detector}_deeptrig_{deep_trigger}_shallowtrig_{shallow_trigger}.csv', 
    delimiter=',', skip_header=1, 
    names=['logE', 'veff', 'dveff', 'sveff', 'coincveff', 'aeff', 'daeff', 'saeff', 'coincaeff', 'fdeep', 'fshallow', 'fcoinc'])
energies = np.power(10.,data_baseline['logE'])

limit_hex = fluxes.get_limit_e2_flux(energy=energies*units.eV, 
                                        veff_sr=data_baseline['veff']*units.km**3*units.sr, 
                                        livetime=livetime*uptime, upperLimOnEvents=1)
l1, = ax.plot(energies/limits.plotUnitsEnergy, limit_hex/limits.plotUnitsFlux, 
    'C2--', linewidth=3, 
    label='{}, {} yrs, {}% uptime'.format(detector,livetime/units.year, uptime*100))

detector = detectors[2]
data_hex = np.genfromtxt(f'results/veff_{detector}_deeptrig_{deep_trigger}_shallowtrig_{shallow_trigger}.csv', 
    delimiter=',', skip_header=1, 
    names=['logE', 'veff', 'dveff', 'sveff', 'coincveff', 'aeff', 'daeff', 'saeff', 'coincaeff', 'fdeep', 'fshallow', 'fcoinc'])
energies = np.power(10.,data_hex['logE'])

limit_hex = fluxes.get_limit_e2_flux(energy=energies*units.eV, 
                                        veff_sr=data_hex['veff']*units.km**3*units.sr, 
                                        livetime=livetime*uptime, upperLimOnEvents=1)
l2, = ax.plot(energies/limits.plotUnitsEnergy, limit_hex/limits.plotUnitsFlux, 
    'C1-.', linewidth=3,
    label='{}, {} yrs, {}% uptime'.format(detector,livetime/units.year, uptime*100))

detector = detectors[4]
deep_trigger = 'review'
shallow_trigger = 'review'
data_review = np.genfromtxt(f'results/veff_{detector}_deeptrig_{deep_trigger}_shallowtrig_{shallow_trigger}.csv', 
    delimiter=',', skip_header=1, 
    names=['logE', 'veff', 'dveff', 'sveff', 'coincveff', 'aeff', 'daeff', 'saeff', 'coincaeff', 'fdeep', 'fshallow', 'fcoinc'])
energies = np.power(10.,data_review['logE'])

limit_review = fluxes.get_limit_e2_flux(energy=energies*units.eV, 
                                        veff_sr=data_review['veff']*units.km**3*units.sr, 
                                        livetime=livetime*uptime, upperLimOnEvents=1)
l3, = ax.plot(energies/limits.plotUnitsEnergy, limit_review/limits.plotUnitsFlux, 
    'C4:', linewidth=3,
    label='{}, {} yrs, {}% uptime'.format(detector,livetime/units.year, uptime*100))


ax.plot([np.power(10., 17.5), np.power(10., 19)], [3E-10, 3E-10], 'r-', linewidth=3)
ax.plot([30E15], [1E-9], 'rx', markersize=10, markeredgewidth=3)

ax.legend(handles=[l1, l2, l3], loc='upper right')
ax.set_ylim([1E-10, 1E-8])
ax.set_xlim([1E15, 1E21])
ax.set_title('Trigger Level')
fig.savefig('limit_v2.png')