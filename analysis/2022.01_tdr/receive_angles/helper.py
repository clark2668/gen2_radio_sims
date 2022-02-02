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

    ugids, uindex = np.unique(np.array(fin['event_group_ids']), 
        return_index=True)
    the_keys = fin.keys()

    try:
        tnames = fin.attrs['trigger_names']
    except:
        return None, None
    
    tname_to_index = {}
    for i, key in enumerate(tnames):
        tname_to_index[key] = i

    all_thetas = []
    max_amp_thetas = []

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
                rec_vec = s['receive_vectors']
                amps = s['max_amp_shower_and_ray']
                # print('Shower ids {}, Mask {}, Rec Vectors {}'.format(shower_ids, trigger_mask, rec_vec))
                # print('{}, {}'.format(rec_vec, type))

                # trig_showers = shower_ids[trigger_mask]
                # the following slice grabs the last 8 antennas (4:)
                # and the 2 solutions * 3 elements of the array
                # without the 4:, this would have shape n_channels * n_solutions * 3
                trig_rec_vec = rec_vec[trigger_mask, 4:] 
                trig_amps = amps[trigger_mask, 4:]
                
                for shower_amps, shower_vecs in zip(trig_amps, trig_rec_vec):
                    temp_amps = np.asarray(shower_amps)
                    temp_rec_angs = np.asarray(shower_vecs)
                    max_element = np.nanmax(temp_amps)
                    index = np.where(temp_amps==max_element)
                    # print(temp_amps)
                    # print(temp_rec_angs)
                    # print("max element is {}, Index {}".format(max_element, index))
                    the_vec = temp_rec_angs[index][0]
                    temp_theta = np.arccos(the_vec[2])
                    max_amp_thetas.append(temp_theta)
                    # print("The vec {}".format(the_vec))
                

                for shower in trig_rec_vec: 
                    # loop over showers
                    choosy_antenna = shower[4] # choose the middle of the array
                    for vec in choosy_antenna:
                        the_theta = np.arccos(vec[2])
                        all_thetas.append(the_theta)
                        # print(vec)
                    # for ch in shower: # loop over channel
                        # for vec in ch: # loop over solutions
                            # print(vec)
                            # the_theta = np.acos(vec[2])
                            # thetas.append(the_theta)
    

                # trig_rec_vec_deep = trig_rec_vec[4,:]
                # print(trig_rec_vec_deep)

                # for l in trig_rec_vec:
                #     for m in l:
                #         for n in m:
                #             print('    n: {}'.format(n))
                    # print('    l: {}'.format(l))
                # print('  Trig Showers {}'.format(trig_showers))
                # print('  Rec Vecs {}'.format(trig_rec_vec))

                # trig_showers = shower_ids[trigger_mask]
                # print('Trig Showers {}'.format(trig_showers))

                # with_trigs = rec_vec[trigger_mask, :]
                # print("With trig {}".format(len(with_trigs)))
                # print('Rec Vec {}'.format(rec_vec[trigger_mask, :]))

                # print('----')
                # print('\n\n')

    return all_thetas, max_amp_thetas



