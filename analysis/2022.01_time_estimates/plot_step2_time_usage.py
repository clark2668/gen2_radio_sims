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
# detector='hex_hybrid_only'

flav_dict = {
    "e" : 0,
    "mu" : 1,
    "tau" : 2
}

e_times = np.empty((4,20,5))
mu_times = np.empty((4,20,10))
tau_times = np.empty((4,20,10))

times_dict ={
    "e" : e_times,
    "mu" : mu_times,
    "tau" : tau_times
}

def pick_bins(flav, en, czmin):
    en_bin = int((en-18.5)/0.5)
    flav_index = flav_dict[flav]
    zen_bin = int((czmin*10)+10)
    return flav_index, en_bin, zen_bin

def get_num_events(flav, en):
    return 500

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

            num_events = get_num_events(flav, en)

            flav_index, en_index, zen_index = pick_bins(flav, en, czmin)
            # print("En bin {}, zen bin {}, part bin {}, time {}".format(en_index, zen_index, part, timesec))
            times_dict[flavor][en_index][zen_index][part] = timesec/num_events

            # this way we are storing the time per event entered *at step 0*
            # which is the variable we have control over, so forget whatever magic nuradiomc tries to pull

            line = fp.readline()

average_time_dicts ={
    "e" : np.mean(times_dict['e'], axis=2),
    "mu" : np.mean(times_dict['mu'], axis=2),
    "tau" : np.mean(times_dict['tau'], axis=2),
}

# assumed_hours = 2

# times_e = np.divide(assumed_hours*60*60, average_time_dicts['e'])
# times_mu = np.divide(assumed_hours*60*60, average_time_dicts['mu'])
# times_tau = np.divide(assumed_hours*60*60, average_time_dicts['tau'])

# from numpy import inf
# times_e[times_e==inf] = 1e4
# times_mu[times_mu==inf] = 1e4
# times_tau[times_tau==inf] = 1e4

# times_e[times_e>1e4] = 1e4
# times_mu[times_mu>1e4] = 1e4
# times_tau[times_tau>1e4] = 1e4


# num_events_per_run_dict = {
# 	"e" : times_e,
# 	"mu" : times_mu,
# 	"tau" : times_tau
# }


tick_types = ['o', 's', 'v', '^']
color_choices = ['blue', 'orange', 'green', 'red']
# logEs = np.arange(19.0, 19.1, 0.5)

# now to make plots
# we want run time per "main" event vs declination
for flavor in flavors:
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    for iE, logE in enumerate(logEs):
        ax.plot(zenbins[:-1], average_time_dicts[flavor][iE][:],label='{}'.format(logE), marker=tick_types[iE], color=color_choices[iE])
    ax.set_xlabel(r'cos($\theta$)',size=15)
    ax.set_ylabel(r'Seconds Per Event',size=15)
    if flavor=='e':
        ax.set_ylim([0,10])
    else:
        ax.set_ylim([0,10])
    ax.set_title('time per event for nu-{} in {}'.format(flavor, detector),size=15)
    ax.tick_params(labelsize=15)
    ax.legend()
    fig.savefig("time_per_event_{}_{}.png".format(detector, flavor),edgecolor='none', bbox_inches='tight')


# # and plot number of events per run to fit in 3.5 hours
# for flavor in flavors:
# 	print(flavor)
# 	fig = plt.figure(figsize=(10,5))
# 	ax = fig.add_subplot(111)
# 	for iE, logE in enumerate(logEs):
# 		ax.plot(zenbins[5:-1], num_events_per_run_dict[flavor][iE][5:],label='{}'.format(logE), marker=tick_types[iE],color=color_choices[iE])
# 		# slope, intercept, r_value, p_value, std_err = stats.linregress(zenbins[10:-1], num_events_per_run_dict[flavor][iE][10:])
# 		# dummy_y = zenbins[10:-1]*slope + intercept
# 		# ax.plot(zenbins[10:-1], dummy_y, '--',color=color_choices[iE])
# 		the_xvals = zenbins[10:-1]
# 		the_yvals = num_events_per_run_dict[flavor][iE][10:]
# 		# interpolator = splrep(the_xvals, the_yvals)
# 		# dummy_y = splev(the_xvals, interpolator)
# 		z = np.polyfit(the_xvals, the_yvals,2)
# 		p = np.poly1d(z)
# 		dummy_y = p(the_xvals)
# 		print(logE)
# 		for y in dummy_y:
# 			print(y)
# 		print("")
# 		ax.plot(the_xvals, dummy_y, '--',color=color_choices[iE])


# 	ax.set_xlabel(r'cos($\theta$)',size=15)
# 	ax.set_ylabel(r'Number of Events',size=15)
# 	# ax.set_ylim([0,5000])
# 	ax.set_yscale('log')
# 	ax.set_title('number of 0 events to run in {}hrs for nu-{}'.format(assumed_hours, flavor),size=15)
# 	ax.tick_params(labelsize=15)
# 	ax.legend()
# 	fig.savefig("predicted_num_evts_per_run_{}m_{}.png".format(depth, flavor),edgecolor='none', bbox_inches='tight')

# for flavor in flavors:
# 	print(flavor)
# 	for iZ in range(len(zenbins)-1):
# 		print("{:.1f}, {:.1f}, {}, {}, {}, {}".format(zenbins[iZ], zenbins[iZ + 1],
# 			num_events_per_run_dict[flavor][0][iZ],
# 			num_events_per_run_dict[flavor][1][iZ],
# 			num_events_per_run_dict[flavor][2][iZ],
# 			num_events_per_run_dict[flavor][3][iZ]))

