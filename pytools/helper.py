import numpy as np


def get_coszenbins():
	return np.linspace(-1,1,21)

def get_logEs():
	return np.arange(18.5, 20.1, 0.5)

# def get_number_of_parts_and_events(flavor, logE):
# 	num_parts=1
# 	num_events=1
# 	splitter=20

	
# 	if flavor=='e':
# 		# the electron flavor is always fast, and can always take 1000 events
# 		num_parts=int(100/splitter)
# 		num_events=100
# 	elif flavor=='mu' or flavor=='tau':
# 		# otherwise, we need to be clever about energy bins
# 		if logE<18:
# 			num_parts=int(100/splitter)
# 			num_events=500
# 		elif logE>=18 and logE<19:
# 			num_parts=int(200/splitter)
# 			num_events=25
# 		elif logE>=19:
# 			num_parts=int(200/splitter)
# 			num_events=15

# 	return num_parts, num_events

def get_number_of_parts_and_events(flavor, logE, czmin):
	num_parts=1
	num_events=1
	
	if flavor=='e':
		# the electron flavor is always fast, and can always take 1000 events
		if czmin < -0.5:
			num_events = int(10000)
			num_parts = int(10)
		else:
			num_events = int(5000)
			num_parts = int(20)
	elif flavor=='mu' or flavor=='tau':
		# otherwise, be clever

		if czmin < -0.3:
			num_events = int(10000)
			num_parts = int(10)
		
		else if (czmin < 0.4 and czmin >=-0.3 ):
			if logE<19:
				num_events = int(250)
				num_parts = int(400)
			else if (logE<19.5 and logE>=19):
				num_events = int(100)
				num_parts = int(1000)
			else if (logE<20 and logE>=19.5):
				num_events = int(50)
				num_parts = int(2000)
			else if (logE>=20):
				num_events = int(25)
				num_parts = int(4000)
		
		else if (czmin >= 0.4 ):
			if logE<19:
				num_events = int(1000)
				num_parts = int(100)
			else if (logE<19.5 and logE>=19):
				num_events = int(500)
				num_parts = int(200)
			else if (logE<20 and logE>=19.5):
				num_events = int(250)
				num_parts = int(400)
			else if (logE>=20):
				num_events = int(100)
				num_parts = int(1000)

	return num_parts, num_events