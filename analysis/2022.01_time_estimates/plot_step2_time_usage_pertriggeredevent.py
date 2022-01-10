import numpy as np
from pytimeparse.timeparse import timeparse
import matplotlib.pyplot as plt
import sys
from scipy import stats
from scipy.interpolate import interp1d, splrep, splev

zenbins = np.linspace(-1, 1, 21)
logEs = np.arange(18.5, 20.1, 0.5)
# logEs = np.arange(19.0, 19.1, 0.5)
print(logEs)

energies = 10 ** logEs
flavors = ["e", "mu", "tau"]

detector='baseline'
detector='hex_hybrid_only'

flav_dict = {
    "e" : 0,
    "mu" : 1,
    "tau" : 2
}

e_times = np.zeros((4,20)) # energy then zen bin
mu_times = np.zeros((4,20))
tau_times = np.zeros((4,20))

e_counts = np.zeros((4,20))
mu_counts = np.zeros((4,20))
tau_counts = np.zeros((4,20))

times_dict ={
    "e" : e_times,
    "mu" : mu_times,
    "tau" : tau_times
}

counts_dict ={
    "e" : e_counts,
    "mu" : mu_counts,
    "tau" : tau_counts
}

def pick_bins(flav, en, czmin):
    en_bin = int((en-18.5)/0.5)
    flav_index = flav_dict[flav]
    zen_bin = int((czmin*10)+10)
    return flav_index, en_bin, zen_bin

def get_num_events(flav, en):
    return 500

# first, weneed to populate the times dictionary

for flavor in flavors:
    file = "times_" + detector + "_array_"+ flavor + ".txt"
    with open(file) as fp:
        line = fp.readline()
        while line:
            split_line = line.strip().split(':')
            type_info = split_line[0]
            time_info = split_line[-1]

            # first is type info
            split_time_info = time_info.strip().split(' ')
            the_time = split_time_info[4]
            timesec = timeparse(the_time)

            # 0 = step1, 1 = flavor, 2 = 20, 3 = 00, 
            # 4 = dipoles_RNOG_20m
            # 5 = 00km
            # 6 = czmin major, 7 = czmin minor
            # 8 = czmax major, 9 = czmax minor
            # 10 = part, # 11 = throw away, #12 throw away

            split_type = type_info.split('.')
            flav = split_type[1]
            en = split_type[2] + '.' + split_type[3]
            czmin = split_type[5] + '.' + split_type[6]
            part = int(split_type[10])

            en = float(en)
            czmin = float(czmin)

            # num_events = get_num_events(flav, en)

            flav_index, en_index, zen_index = pick_bins(flav, en, czmin)
            # print("En bin {}, zen bin {}, part bin {}, time {}".format(en_index, zen_index, part, timesec))
            times_dict[flavor][en_index][zen_index] += timesec

            line = fp.readline()


# now the number of events

for flavor in flavors:
    file = "triggers_" + detector + "_array_"+ flavor + ".txt"
    with open(file) as fp:
        line = fp.readline()
        while line:
            split_line = line.strip().split(':')
            type_info = split_line[0]
            trigger_info = split_line[-1]

            # first is time info
            split_trigger_info = trigger_info.strip().split(' ')
            the_triggers = split_trigger_info[5]
            the_triggers = the_triggers.strip().split('/')
            triggered = int(the_triggers[0])
            thrown = int(the_triggers[1])
            triggered = 500

            # 0 = step1, 1 = flavor, 2 = 20, 3 = 00, 
            # 4 = dipoles_RNOG_20m
            # 5 = 00km
            # 6 = czmin major, 7 = czmin minor
            # 8 = czmax major, 9 = czmax minor
            # 10 = part, # 11 = throw away, #12 throw away

            split_type = type_info.split('.')
            flav = split_type[1]
            en = split_type[2] + '.' + split_type[3]
            czmin = split_type[5] + '.' + split_type[6]
            part = int(split_type[10])

            en = float(en)
            czmin = float(czmin)

            flav_index, en_index, zen_index = pick_bins(flav, en, czmin)
            print("En bin {}, zen bin {}, part bin {}, triggers {}".format(en_index, zen_index, part, triggered))
            counts_dict[flavor][en_index][zen_index] += triggered

            line = fp.readline()

average_time_dicts={
    "e" : times_dict["e"]/counts_dict["e"],
    "mu" : times_dict["mu"]/counts_dict["mu"],
    "tau" : times_dict["tau"]/counts_dict["tau"]
}
average_time_dicts["e"][np.isnan(average_time_dicts["e"])] = 0
average_time_dicts["e"][np.isinf(average_time_dicts["e"])] = 0
average_time_dicts["mu"][np.isnan(average_time_dicts["mu"])] = 0
average_time_dicts["mu"][np.isinf(average_time_dicts["mu"])] = 0
average_time_dicts["tau"][np.isnan(average_time_dicts["tau"])] = 0
average_time_dicts["tau"][np.isinf(average_time_dicts["tau"])] = 0

# print(times_dict["e"])
# print(counts_dict["e"])
# print(average_time_dicts["e"])

tick_types = ['o', 's', 'v', '^']
color_choices = ['blue', 'orange', 'green', 'red']

# now to make plots
# we want run time per "triggered" event vs declination
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)
for iflavor, flavor in enumerate(flavors):
    # fig = plt.figure(figsize=(10,5))
    # ax = fig.add_subplot(111)
    # for iE, logE in enumerate(logEs):
        # ax.plot(zenbins[:-1], average_time_dicts[flavor][iE][:],label='{}'.format(logE), marker=tick_types[iE], color=color_choices[iE])
    ax.plot(zenbins[:-1], average_time_dicts[flavor][1][:], label='{}'.format(flavor), marker=tick_types[iflavor], color=color_choices[iflavor])
    ax.set_xlabel(r'cos($\theta$)',size=15)
    ax.set_ylabel(r'Seconds Per Requested Primary',size=15)
    # if flavor=='e':
    #     ax.set_ylim([0,10])
    # else:
    #     ax.set_ylim([0,10])
    ax.set_ylim([0, 150])
    ax.set_xlim([-1.2, 1.2])
    # ax.set_title('time per requested primary for nu-{} in {}'.format(flavor, detector),size=15)
    ax.tick_params(labelsize=15)
    ax.legend()
    # fig.savefig("time_per_event_{}_{}.png".format(detector, flavor),edgecolor='none', bbox_inches='tight')
ax.set_title('time per requested primary for {}'.format(detector),size=15)
fig.savefig("time_per_event_{}.png".format(detector),edgecolor='none', bbox_inches='tight')

# number of triggered events (not weights, grr) vs declination
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)
for iflavor, flavor in enumerate(flavors):
    ax.plot(zenbins[:-1], counts_dict[flavor][1][:], label='{}'.format(flavor), marker=tick_types[iflavor], color=color_choices[iflavor])
    ax.set_xlabel(r'cos($\theta$)',size=15)
    ax.set_ylabel(r'Seconds Per Requested Primary',size=15)
    # ax.set_ylim([0, 150])
    ax.set_xlim([-1.2, 1.2])
    ax.tick_params(labelsize=15)
    ax.legend()
ax.set_title('counts for {}'.format(detector),size=15)
fig.savefig("counts_{}.png".format(detector),edgecolor='none', bbox_inches='tight')


# # # and plot number of events per run to fit in 3.5 hours
# # for flavor in flavors:
# # 	print(flavor)
# # 	fig = plt.figure(figsize=(10,5))
# # 	ax = fig.add_subplot(111)
# # 	for iE, logE in enumerate(logEs):
# # 		ax.plot(zenbins[5:-1], num_events_per_run_dict[flavor][iE][5:],label='{}'.format(logE), marker=tick_types[iE],color=color_choices[iE])
# # 		# slope, intercept, r_value, p_value, std_err = stats.linregress(zenbins[10:-1], num_events_per_run_dict[flavor][iE][10:])
# # 		# dummy_y = zenbins[10:-1]*slope + intercept
# # 		# ax.plot(zenbins[10:-1], dummy_y, '--',color=color_choices[iE])
# # 		the_xvals = zenbins[10:-1]
# # 		the_yvals = num_events_per_run_dict[flavor][iE][10:]
# # 		# interpolator = splrep(the_xvals, the_yvals)
# # 		# dummy_y = splev(the_xvals, interpolator)
# # 		z = np.polyfit(the_xvals, the_yvals,2)
# # 		p = np.poly1d(z)
# # 		dummy_y = p(the_xvals)
# # 		print(logE)
# # 		for y in dummy_y:
# # 			print(y)
# # 		print("")
# # 		ax.plot(the_xvals, dummy_y, '--',color=color_choices[iE])


# # 	ax.set_xlabel(r'cos($\theta$)',size=15)
# # 	ax.set_ylabel(r'Number of Events',size=15)
# # 	# ax.set_ylim([0,5000])
# # 	ax.set_yscale('log')
# # 	ax.set_title('number of 0 events to run in {}hrs for nu-{}'.format(assumed_hours, flavor),size=15)
# # 	ax.tick_params(labelsize=15)
# # 	ax.legend()
# # 	fig.savefig("predicted_num_evts_per_run_{}m_{}.png".format(depth, flavor),edgecolor='none', bbox_inches='tight')

# # for flavor in flavors:
# # 	print(flavor)
# # 	for iZ in range(len(zenbins)-1):
# # 		print("{:.1f}, {:.1f}, {}, {}, {}, {}".format(zenbins[iZ], zenbins[iZ + 1],
# # 			num_events_per_run_dict[flavor][0][iZ],
# # 			num_events_per_run_dict[flavor][1][iZ],
# # 			num_events_per_run_dict[flavor][2][iZ],
# # 			num_events_per_run_dict[flavor][3][iZ]))

