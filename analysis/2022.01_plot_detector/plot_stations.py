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

def plot_pa_passband():

    # passbands for the phasing
    passband_low = [96 * units.MHz, 100 * units.GHz]
    passband_high = [0 * units.MHz, 220 * units.MHz]
    order_low = 4
    order_high = 7
    ripple = 0.1
    filter_type = 'cheby1'

    ff = np.fft.rfftfreq(1024, 0.5 * units.ns)

    mask = ff > 0
    b_low, a_low = scipy.signal.cheby1(order_low, ripple, passband_low, 'bandpass', analog=True)
    w_low, h_low = scipy.signal.freqs(b_low, a_low, ff[mask])
    b_hi, a_hi = scipy.signal.cheby1(order_high, ripple, passband_high, 'bandpass', analog=True)
    w_hi, h_hi = scipy.signal.freqs(b_hi, a_hi, ff[mask])

    filt = h_low * h_hi
    gain = np.abs(filt)
    phase = np.angle(filt)
    unwrap = np.unwrap(phase)
    dF = ff[1]-ff[0]
    group_delay = np.diff(unwrap)/dF

    fig, axs_filt = plt.subplots(1, 3, figsize=(10,5))
    axs_filt[0].plot(ff[1:]/units.MHz, 20.*np.log10(gain), color='k')
    axs_filt[0].set_xlabel("Frequency [MHz]")
    axs_filt[0].set_ylabel("Gain [dB]")

    axs_filt[1].plot(ff[1:]/units.MHz, unwrap, color='k')
    axs_filt[1].set_xlabel("Frequency [MHz]")
    axs_filt[1].set_ylabel("Unwrapped Phase")

    axs_filt[2].plot(ff[2:]/units.MHz, group_delay, color='k')
    axs_filt[2].set_xlabel("Frequency [MHz]")
    axs_filt[2].set_ylabel("Group Delay [ns]")
    fig.tight_layout()

    fig.subplots_adjust(top=0.9)
    axs_filt[0].set_xlim(0, 300)
    axs_filt[0].set_ylim([-10,1])
    axs_filt[1].set_xlim(0,300)
    axs_filt[2].set_xlim(0,300)
    fig.suptitle("PA Trigger Antenna Filter")
    fig.savefig('pa_filter.png', dpi=300, edgecolor='none', bbox_inches='tight')

def plot_lpda_passband():

    # passbands for the phasing
    passband_low = [1 * units.MHz, 0.15*units.GHz]
    passband_high = [ 0.08*units.GHz, 800 * units.GHz]
    order_low = 10
    order_high = 5
    ripple = 0.1
    filter_type = 'cheby1'

    ff = np.fft.rfftfreq(1024, 0.5 * units.ns)

    mask = ff > 0
    b_low, a_low = scipy.signal.butter(order_low, passband_low, 'bandpass', analog=True)
    w_low, h_low = scipy.signal.freqs(b_low, a_low, ff[mask])
    b_hi, a_hi = scipy.signal.butter(order_high, passband_high, 'bandpass', analog=True)
    w_hi, h_hi = scipy.signal.freqs(b_hi, a_hi, ff[mask])

    filt = h_low * h_hi
    gain = np.abs(filt)
    phase = np.angle(filt)
    unwrap = np.unwrap(phase)
    dF = ff[1]-ff[0]
    group_delay = np.diff(unwrap)/dF

    fig, axs_filt = plt.subplots(1, 3, figsize=(10,5))
    axs_filt[0].plot(ff[1:]/units.MHz, 20.*np.log10(gain), color='k')
    axs_filt[0].set_xlabel("Frequency [MHz]")
    axs_filt[0].set_ylabel("Gain [dB]")

    axs_filt[1].plot(ff[1:]/units.MHz, unwrap, color='k')
    axs_filt[1].set_xlabel("Frequency [MHz]")
    axs_filt[1].set_ylabel("Unwrapped Phase [rad]")

    axs_filt[2].plot(ff[2:]/units.MHz, group_delay, color='k')
    axs_filt[2].set_xlabel("Frequency [MHz]")
    axs_filt[2].set_ylabel("Group Delay [ns]")
    fig.tight_layout()

    fig.subplots_adjust(top=0.9)
    axs_filt[0].set_xlim(0, 300)
    axs_filt[0].set_ylim([-10,1])
    axs_filt[1].set_xlim(0,300)
    axs_filt[2].set_xlim(0,300)
    axs_filt[2].set_ylim(-200,10)
    fig.suptitle("LPDA Trigger Antenna Filter")
    fig.savefig('lpda_filter.png', dpi=300, edgecolor='none', bbox_inches='tight')


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