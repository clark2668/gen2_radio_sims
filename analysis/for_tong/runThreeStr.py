import argparse
# import detector simulation modules
import NuRadioReco.modules.trigger.highLowThreshold
import NuRadioReco.modules.trigger.simpleThreshold
import NuRadioReco.modules.channelBandPassFilter
import NuRadioReco.modules.triggerTimeAdjuster
from NuRadioReco.utilities import units
import yaml
import numpy as np
from scipy import constants
from NuRadioMC.simulation import simulation
import scipy
import matplotlib.pyplot as plt
import logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("runThreeStr")

simpleThreshold = NuRadioReco.modules.trigger.simpleThreshold.triggerSimulator()
highLowThreshold = NuRadioReco.modules.trigger.highLowThreshold.triggerSimulator()
channelBandPassFilter = NuRadioReco.modules.channelBandPassFilter.channelBandPassFilter()

class mySimulation(simulation.simulation):

    def _detector_simulation_filter_amp(self, evt, station, det):
        channelBandPassFilter.run(evt, station, det, passband=[80 * units.MHz, 1000 * units.GHz], filter_type="butter", order=2)
        channelBandPassFilter.run(evt, station, det, passband=[0 * units.MHz, 500 * units.MHz], filter_type="butter", order=10)

    def _detector_simulation_trigger(self, evt, station, det):
        #run a high/low trigger on the deep bicones
        highLowThreshold.run(evt, station, det,
                                    threshold_high=2. * self._Vrms_per_channel[station.get_id()][0],
                                    threshold_low=-2. * self._Vrms_per_channel[station.get_id()][0],
                                    triggered_channels=[0, 1, 2, 3, 4, 5, 6, 7, 8], # select the bicone channels
                                    number_concidences=1, # 4/12 majority logic
                                    coinc_window=270 * units.ns,
                                    trigger_name='deep_bicones_1of6_2sigma') # calculate more time consuming ARIANNA trigger only if station passes simple trigger

parser = argparse.ArgumentParser(description='Run NuRadioMC simulation')
parser.add_argument('inputfilename', type=str,
                    help='path to NuRadioMC input event list')
parser.add_argument('detectordescription', type=str,
                    help='path to file containing the detector description')
parser.add_argument('config', type=str,
                    help='NuRadioMC yaml config file')
parser.add_argument('outputfilename', type=str,
                    help='hdf5 output filename')
parser.add_argument('outputfilenameNuRadioReco', type=str, nargs='?', default=None,
                    help='outputfilename of NuRadioReco detector sim file')
args = parser.parse_args()

sim = mySimulation(inputfilename = args.inputfilename,
                            outputfilename = args.outputfilename,
                            detectorfile = args.detectordescription,
                            outputfilenameNuRadioReco = args.outputfilenameNuRadioReco,
                            config_file = args.config,
                            file_overwrite = True)

sim.run()

