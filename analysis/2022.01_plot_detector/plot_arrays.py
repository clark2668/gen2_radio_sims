from asyncore import write
from NuRadioReco.detector import generic_detector
import numpy as np
import matplotlib.pyplot as plt

scale=1000
top_dir = "/home/brianclark/Gen2/radio/analysis-scripts/gen2-tdr-2021/detector"

detectors = [
    "trigger_Gen2_baseline_array.json",
    "trigger_Gen2_hex_hybrid_only_array.json",
    "trigger_Gen2_hex_shallow_array.json",
    "trigger_Gen2_hex_shallowheavy_array.json"
]

det_names = {
    "trigger_Gen2_baseline_array.json" : "Baseline",
    "trigger_Gen2_hex_hybrid_only_array.json" : "Hybrid Only",
    "trigger_Gen2_hex_shallow_array.json" : "Hex Shallow",
    "trigger_Gen2_hex_shallowheavy_array.json" : "Hex Shallow-Heavy"
}

det_shortnames = {
    "trigger_Gen2_baseline_array.json" : "baseline_array",
    "trigger_Gen2_hex_hybrid_only_array.json" : "hex_hybrid_only_array",
    "trigger_Gen2_hex_shallow_array.json" : "hex_shallow_array",
    "trigger_Gen2_hex_shallowheavy_array.json" : "hex_shallowheavy_array"
}

write_files = True
if write_files:
    for detfile in detectors:

        hybrid_list = []
        shallow_list = []

        det = generic_detector.GenericDetector(json_filename=top_dir+'/'+detfile, 
            create_new = True)
        for station_id in det.get_station_ids():
            station = det.get_station(station_id)
            if station['reference_station'] == 1001:
                hybrid_list.append(station_id)
            elif station['reference_station'] == 2001:
                shallow_list.append(station_id)

        f = open(f'stations_{det_shortnames[detfile]}_hybrid.csv', 'w')
        for h in hybrid_list:
            f.write('{}\n'.format(h))
        f.close()

        f = open(f'stations_{det_shortnames[detfile]}_shallow.csv', 'w')
        for s in shallow_list:
            f.write('{}\n'.format(s))
        f.close()


make_plot = False
if make_plot:
    for detfile in detectors:

        surf_x = []
        surf_y = []
        hybrid_x = []
        hybrid_y = []

        det = generic_detector.GenericDetector(json_filename=top_dir+'/'+detfile, 
            create_new = True)
        for station_id in det.get_station_ids():
            pos = det.get_absolute_position(station_id)
            station = det.get_station(station_id)

            if station['reference_station'] == 1001:
                hybrid_x.append(pos[0]/scale) 
                hybrid_y.append(pos[1]/scale)
            elif station['reference_station'] == 2001:
                surf_x.append(pos[0]/scale) 
                surf_y.append(pos[1]/scale)
        
        fig, axs = plt.subplots(1, 1, figsize=(5,5))
        if len(surf_x) > 0:
            axs.plot(surf_x, surf_y, 'C1s', label='Shallow Station', markersize=2)
        if len(hybrid_x) > 0:
            axs.plot(hybrid_x, hybrid_y, 'C0o', label='Hybrid Station', markersize=3)
        axs.set_xlabel("Easting [km]", size=15)
        axs.set_ylabel("Northing [km]", size=15)
        axs.set_xlim([-25, 25])
        axs.set_ylim([-25, 25])
        axs.tick_params(labelsize=15)
        axs.set_title(det_names[detfile], size=15)
        axs.legend(loc='lower right')
        axs.set_aspect('equal')
        fig.tight_layout()
        fig.savefig('plots/array_{}.pdf'.format(det_shortnames[detfile]), dpi=300)

