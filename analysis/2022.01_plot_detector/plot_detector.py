import sys
import NuRadioReco.detector.detector as detector
from NuRadioReco.detector import generic_detector
from NuRadioReco.utilities import units
from astropy.time import Time
import numpy as np
import matplotlib.pyplot as plt
import scipy as scipy
import logging
logging.basicConfig(level=logging.INFO)

def plot_deep_detectors():
    scale=1000

    fig_deep, axs_deep = plt.subplots(1, 2, figsize=(10,5))
    markers = ['o', 'x']

    deep_station_id = 1001

    top_dir = "/Users/brianclark/Documents/work/Gen2/radio/analysis-scripts/gen2-tdr-2021/detector"
    det_file = 'trigger_Gen2_baseline_array.json'
    

    det = generic_detector.GenericDetector(json_filename=top_dir+'/'+det_file)
    n_channels = det.get_number_of_channels(deep_station_id)
    print("Number of channels is {}".format(n_channels))

    lpda_channels = [0, 1, 2, 3]
    eightch_pa_channels = [4, 5, 6, 7, 8, 9, 10, 11]
    fourch_pa_channels = [6, 7, 8, 9]

    # side view
    side_x = []
    side_z = []

    for ch in eightch_pa_channels:
        loc = det.get_relative_position(deep_station_id, ch) # + det.get_absolute_position(deep_station_id)
        side_x.append(0)
        side_z.append(loc[2])
    
    axs_deep[1].plot(side_x, side_z, 'kd', label='8 ch PA', markersize=12)

    side_x.clear()
    side_z.clear()

    for ch in fourch_pa_channels:
        loc = det.get_relative_position(deep_station_id, ch) # + det.get_absolute_position(deep_station_id)
        side_x.append(0)
        side_z.append(loc[2])
    
    axs_deep[1].plot(side_x, side_z, 'rx', label='4 ch PA', markersize=12)


    # top down view
    local_x_lpda = []
    local_y_lpda = []
    county = 0
    for ch in lpda_channels:
        loc = det.get_relative_position(deep_station_id, ch)
        the_x = loc[0]
        the_y = loc[1]
        x_for_plotting = []
        y_for_plotting = []
        if abs(the_y) > 1:
            x_for_plotting.append(the_x+0.5)
            x_for_plotting.append(the_x-0.5)
            y_for_plotting.append(the_y)
            y_for_plotting.append(the_y)
        else:
            x_for_plotting.append(the_x)
            x_for_plotting.append(the_x)
            y_for_plotting.append(the_y+0.5)
            y_for_plotting.append(the_y-0.5)            
        
        if county == 0:
            axs_deep[0].plot(x_for_plotting, y_for_plotting, 'C0', linewidth=4, 
                label='LPDA')
            county+=1
        else:
            axs_deep[0].plot(x_for_plotting, y_for_plotting, 'C0', linewidth=4)

    axs_deep[0].plot([0], [0], 'ro', label='PA String')

    # top down view
    axs_deep[0].set_title("Top Down View", size=15)
    axs_deep[0].set_xlabel(r'X [m]', size=15)
    axs_deep[0].set_ylabel(r'Y [m]', size=15)
    # axs_deep[1].set_xlim([-2.5, 2.5])
    axs_deep[0].legend(loc='lower left')
    axs_deep[0].tick_params(labelsize=15)
    axs_deep[0].set_aspect('equal')

    # side view
    axs_deep[1].set_title("Side View of PA", size=15)
    axs_deep[1].set_xlabel(r'X [m]', size=15)
    axs_deep[1].set_ylabel(r'Depth [m]', size=15)
    axs_deep[1].set_xlim([-2.5, 2.5])
    axs_deep[1].legend(loc='lower left')
    axs_deep[1].tick_params(labelsize=15)
    
    plt.tight_layout(pad=3.0)
    fig_deep.savefig('plots/deep_detector.pdf')


def plot_shallow_detectors():
    scale=1000

    fig_shallow, axs_shallow = plt.subplots(1, 1, figsize=(5,5))

    shallow_station_id = 2001

    top_dir = "/Users/brianclark/Documents/work/Gen2/radio/analysis-scripts/gen2-tdr-2021/detector"
    det_file = 'trigger_Gen2_baseline_array.json'
    
    det = generic_detector.GenericDetector(json_filename=top_dir+'/'+det_file)
    n_channels = det.get_number_of_channels(shallow_station_id)

    lpda_channels = [0, 1, 2, 3]

    # top down view is the only one that makes sense
    local_x_lpda = []
    local_y_lpda = []
    county = 0
    for ch in lpda_channels:
        loc = det.get_relative_position(shallow_station_id, ch)
        the_x = loc[0]
        the_y = loc[1]
        x_for_plotting = []
        y_for_plotting = []
        if abs(the_y) > 1:
            x_for_plotting.append(the_x+0.5)
            x_for_plotting.append(the_x-0.5)
            y_for_plotting.append(the_y)
            y_for_plotting.append(the_y)
        else:
            x_for_plotting.append(the_x)
            x_for_plotting.append(the_x)
            y_for_plotting.append(the_y+0.5)
            y_for_plotting.append(the_y-0.5)            
        
        if county == 0:
            axs_shallow.plot(x_for_plotting, y_for_plotting, 'C0', linewidth=4, 
                label='LPDA')
            county+=1
        else:
            axs_shallow.plot(x_for_plotting, y_for_plotting, 'C0', linewidth=4)

    # top down view
    axs_shallow.set_title("Top Down View", size=15)
    axs_shallow.set_xlabel(r'X [m]', size=15)
    axs_shallow.set_ylabel(r'Y [m]', size=15)
    axs_shallow.legend(loc='lower left')
    axs_shallow.tick_params(labelsize=15)
    axs_shallow.set_aspect('equal')
    plt.tight_layout()
    fig_shallow.savefig('plots/shallow_detector.pdf')


plot_deep_detectors()
plot_shallow_detectors()