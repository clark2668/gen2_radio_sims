import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import h5py
import glob
import os
import sys
import pickle
from multiprocessing import Pool

def dig_around(filename, deep_trigger, shallow_trigger, hybrid_list, shallow_list):

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
                trigger_mask = s['multiple_triggers'][:, tname_to_index[deep_trigger]]
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
                trig_rec_vec = rec_vec[trigger_mask, 4:] 
                trig_amps = amps[trigger_mask, 4:]
                trig_ff = focus_factors[trigger_mask, 4:]
                
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
                

                for shower in trig_rec_vec: 
                    # loop over showers
                    choosy_antenna = shower[4] # choose the middle of the array
                    for vec in choosy_antenna:
                        the_theta = np.arccos(vec[2])
                        all_thetas.append(the_theta)

                for ff in trig_ff:
                    choosy_antenna = ff[4]
                    all_ffs.append(choosy_antenna[0]) # dir sol
                    all_ffs.append(choosy_antenna[1]) # refr/refl sol
                    # print("the ff {}".format(the_ff))

                    # print("    *--*")
    

                # print('----')
                # print('\n\n')

    return all_thetas, max_amp_thetas, all_ffs, max_amp_ffs

