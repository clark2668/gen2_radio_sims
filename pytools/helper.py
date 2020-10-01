import numpy as np


def get_coszenbins():
	return np.linspace(-1,1,21)

def get_logEs():
	return np.arange(19., 20.1, 0.5)

def get_number_of_parts_and_events(flavor, logE):
	num_parts=1
	num_events=1
	splitter=20

	
	if flavor=='e':
		# the electron flavor is always fast, and can always take 1000 events
		num_parts=int(100/splitter)
		num_events=100
	elif flavor=='mu' or flavor=='tau':
		# otherwise, we need to be clever about energy bins
		if logE<18:
			num_parts=int(100/splitter)
			num_events=1000
		elif logE>=18 and logE<19:
			num_parts=int(400/splitter)
			num_events=250
		elif logE>=19:
			num_parts=int(200/splitter)
			num_events=15

	return num_parts, num_events
