from shutil import which
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import h5py
import glob
import os
import sys
import pickle
from multiprocessing import Pool
import resource
import tarfile

import NuRadioReco.modules.io.eventReader
from NuRadioReco.framework.parameters import electricFieldParameters as efp
from NuRadioReco.framework.parameters import particleParameters as pp
from NuRadioReco.framework.parameters import channelParameters as cp


def dig_around(filename, the_trigger, hybrid_list, shallow_list):

    # lpda channels = [0, 1, 2, 3]
    # hybrid_station_deep_channels = [4, 5, 6, 7]
    print("Filename {}".format(filename))

    fin = h5py.File(filename, "r")

    the_keys = fin.keys()

    try:
        tnames = fin.attrs['trigger_names']
    except:
        return None, None, None, None
    
    tname_to_index = {}
    for i, key in enumerate(tnames):
        tname_to_index[key] = i

    all_thetas = []
    all_ffs = []
    max_amp_thetas = []
    max_amp_ffs = []

    for key in the_keys:
        if(key.startswith("station")):
            id = int(key.split('_')[1])

            # only check hybrid stations (we're after the phased array)
            if id not in hybrid_list:
                continue

            s = fin[key]

            # need to break this down by shower
            if 'multiple_triggers' in s:
                trigger_mask = s['multiple_triggers'][:, tname_to_index[the_trigger]]
                shower_ids = s['shower_id']
                # print(np.asarray(shower_ids))
                rec_vec = s['receive_vectors']
                focus_factors = s['focusing_factor']
                amps = s['max_amp_shower_and_ray']
                # print('Shower ids {}, Mask {}, Rec Vectors {}'.format(shower_ids, trigger_mask, rec_vec))
                # print('{}, {}'.format(rec_vec, type))

                # the following slice grabs the last 8 antennas (4:)
                # and the 2 solutions * 3 elements of the array
                # without the 4:, this would have shape n_channels * n_solutions * 3

                # updated Feb 6 2022 to also account for LPDA trigger
                which_ant_index_to_check = None
                if 'PA' in the_trigger:
                    trig_rec_vec = rec_vec[trigger_mask, 4:] 
                    trig_amps = amps[trigger_mask, 4:]
                    trig_ff = focus_factors[trigger_mask, 4:]
                    which_ant_index_to_check = 4 # check the middle of the PA
                elif 'LPDA' in the_trigger:
                    trig_rec_vec = rec_vec[trigger_mask, :3] 
                    trig_amps = amps[trigger_mask, :3]
                    trig_ff = focus_factors[trigger_mask, :3]
                    which_ant_index_to_check = 0 # check the very first LPDA

                
                # get the receive angle and focusing factor of the 
                # maximum amplitude shower and ray in the event
                for shower_amps, shower_vecs, ff in zip(trig_amps, trig_rec_vec, trig_ff):
                    temp_amps = np.asarray(shower_amps)
                    temp_rec_angs = np.asarray(shower_vecs)
                    temp_ffs = np.asarray(ff)
                    max_element = np.nanmax(temp_amps)
                    index = np.where(temp_amps==max_element)
                    # print(temp_amps)
                    # print(temp_rec_angs)
                    # print("max element is {}, Index {}".format(max_element, index))
                    the_vec = temp_rec_angs[index][0]
                    temp_theta = np.arccos(the_vec[2])
                    max_amp_thetas.append(temp_theta)
                    # max_amp_ffs
                    the_ff = temp_ffs[index][0]
                    max_amp_ffs.append(the_ff)
                    # print("The vec {}".format(the_vec))
                
                # get all receive angles (all showers, all rays)
                for shower in trig_rec_vec: 
                    # loop over showers
                    choosy_antenna = shower[which_ant_index_to_check] # choose the middle of the array
                    for vec in choosy_antenna:
                        the_theta = np.arccos(vec[2])
                        all_thetas.append(the_theta)

                # get all focusing factors (all showers, call rays)
                for ff in trig_ff:
                    choosy_antenna = ff[which_ant_index_to_check]
                    all_ffs.append(choosy_antenna[0]) # dir sol
                    all_ffs.append(choosy_antenna[1]) # refr/refl sol
                    # print("the ff {}".format(the_ff))

                    # print("    *--*")
    

                # print('----')
                # print('\n\n')

    return all_thetas, max_amp_thetas, all_ffs, max_amp_ffs

def do_stuff(event_reader, the_file_name, the_trigger):
    all_thetas = []
    all_weights = []

    max_amp_thetas = []
    max_amp_weights = []

    valid_list = []
    if 'PA' in the_trigger:
        valid_list = [4, 5, 6, 7, 8, 9, 10, 11]
    elif 'LPDA' in the_trigger:
        valid_list = [0, 1, 2, 3]

    event_reader.begin([the_file_name])
    for iE, event in enumerate(event_reader.run()):
        primary = event.get_primary()
        weight = primary.get_parameter(pp.weight)

        for iStation, station in enumerate(event.get_stations()):
            triggers = station.get_triggers()
            if the_trigger not in triggers:
                continue
            if station.has_triggered(the_trigger):
                sim_station = station.get_sim_station()
                
                # all efields
                efields = sim_station.get_electric_fields()
                for efield in efields:
                    if len(efield.get_channel_ids())>1:
                        print("More channel ids than expected. Get out...")
                    ch_id = efield.get_channel_ids()[0]
                    if ch_id in valid_list:
                        theta = efield.get_parameter(efp.zenith)
                        all_thetas.append(theta)
                        all_weights.append(weight)

                
                # now to get the highest amp
                max_amp_global = -1E-30
                max_id = None

                options = []
                shower_ids = sim_station.get_shower_ids()
                for shower_id in shower_ids:
                    channels = sim_station.get_channels_by_shower_id(shower_id)
                    for channel in channels:
                        ch_id = channel.get_id()
                        options.append(ch_id)
                        if ch_id in valid_list:
                            max_amp = channel.get_parameter(cp.maximum_amplitude)
                            if abs(max_amp) > abs(max_amp_global):
                                max_amp_global = max_amp
                                max_id = channel.get_unique_identifier()
                
                if max_id is None:
                    # print("Max ID is {}, but Options were {}".format(max_id, options))
                    # print("Trig Info: {}".format(station.get_triggers()[the_trigger]))
                    # print('----')
                    # this case is confusing AF and shouldn't really be possible...
                    # but just skip it for now, it seems reasonably rare...
                    continue

                # and retrieve it's properties
                top_ch_id = max_id[0]
                top_shower_id = max_id[1]
                top_rt_id = max_id[2]

                efields = sim_station.get_electric_fields()
                for efield in efields:
                    ch_id = efield.get_channel_ids()[0]
                    if ch_id != top_ch_id:
                        continue
                    shower_id = efield.get_shower_id()
                    if shower_id != top_shower_id:
                        continue
                    rt_id = efield.get_ray_tracing_solution_id()
                    if rt_id != top_rt_id:
                        continue
                    max_amp_thetas.append(efield.get_parameter(efp.zenith))
                    max_amp_weights.append(weight)
                
    return all_thetas, all_weights, max_amp_thetas, max_amp_weights

def parallel_process(filename, the_trigger):

    # print("Working on file {}".format(filename))

    all_thetas = []
    all_weights = []
    max_amp_thetas = []
    max_amp_weights = []
    event_reader = NuRadioReco.modules.io.eventReader.eventReader()

    if '.tar.gz' in filename:
        tar = tarfile.open(filename, "r:gz")
        for member in tar.getmembers():
            if member.isfile():
                f_extracted = tar.extract(member)
                all_thetas, all_weights, max_amp_thetas, max_amp_weights = do_stuff(event_reader, member.name, the_trigger)
                os.remove(member.name)
    else:
        all_thetas, all_weights, max_amp_thetas, max_amp_weights = do_stuff(event_reader, filename, the_trigger)
    
    outputs = {}
    outputs['all_thetas'] = all_thetas
    outputs['all_weights'] = all_weights
    outputs['max_amp_thetas'] = max_amp_thetas
    outputs['max_amp_weights'] = max_amp_weights

    return outputs
