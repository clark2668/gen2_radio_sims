import numpy as np
from pytimeparse.timeparse import timeparse

zenbins = np.linspace(-1, 1, 21)
logEs = np.arange(19., 20.1, 0.5)
energies = 10 ** logEs
flavors = ["e", "mu", "tau"]

# for iC in range(len(zenbins)-1):
# 	czen1 = zenbins[iC]
# 	czen2 = zenbins[iC+1]
# 	print("Bin {} czmin {:1f}".format(iC, czen1))

flav_dict = {
	"e" : 0,
	"mu" : 1,
	"tau" : 2
}

e_times = np.empty((3,20,5))
mu_times = np.empty((3,20,10))
tau_times = np.empty((3,20,10))

times_dict ={
	"e" : e_times,
	"mu" : mu_times,
	"tau" : tau_times
}

def pick_bins(flav, en, czmin):
	en = float(en)
	en_bin = int((en-19)/0.5)
	czmin = float(czmin)
	flav_index = flav_dict[flav]
	zen_bin = int((czmin*10)+10)
	return flav_index, en_bin, zen_bin 

for flavor in flavors:
	file = "step1_" + flavor + "_stats.txt"
	with open(file) as fp:
		line = fp.readline()
		while line:
			split_line = line.strip().split(':')
			type_info = split_line[0]
			time_info = split_line[4]
			timesec = timeparse(time_info)

			# 0 = step1, 1 = flavor, 2 = 20, 3 = 00, 
			# 4 = czmin major, 5 = czmin minor
			# 6 = czmax major, 7 = czmax minor
			# 8 = part, # 9 = throw away, #10 throw away

			split_type = type_info.split('.')
			flav = split_type[1]
			en = split_type[2] + '.' + split_type[3]
			czmin = split_type[4] + '.' + split_type[5]
			part = int(split_type[8])

			flav_index, en_index, zen_index = pick_bins(flav, en, czmin)
			# print("En bin {}, zen bin {}, part bin {}".format(en_index, zen_index, part))
			times_dict[flavor][en_index][zen_index][part] = timesec

			line = fp.readline()

print(times_dict['mu'])
