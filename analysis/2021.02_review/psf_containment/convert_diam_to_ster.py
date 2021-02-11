import numpy as np
import matplotlib.pyplot as plt

def diameter_to_steradian(sigma, CL): # sigma in degrees, # CL is what confidence level you want, e.g. 50%, 90%, etc.
	
	# get the mahalanobis distance https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118537
	if CL > 1.:
		print("You asked for CL {}, which is greater than one! Setting distance to 1.")
	else:
		dist = np.sqrt(-2. * np.log(1-CL)) * sigma # scale the gaussian error radius by containment
	
	#https://physics.stackexchange.com/questions/457117/why-multiply-by-frac-pi4-when-converting-a-light-sources-angular-diamete
	return np.deg2rad(dist)**2 * np.pi/4

fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)

radii = np.logspace(np.log10(0.05), np.log10(5), num=19)
areas_50 = diameter_to_steradian(radii, 0.5) * (180./np.pi)**2 
areas_90 = diameter_to_steradian(radii, 0.9) * (180./np.pi)**2 
ax.plot(radii, areas_50, label='50% contaiment')
ax.plot(radii, areas_90, label='90% contaiment')
ax.set_xlabel(r'Angular resolution [$\sigma$]')
ax.set_ylabel(r'Area on the sky [deg$^2$]')
ax.legend()
plt.tight_layout()
fig.savefig('conversion.png')

# # ke's plot goes from 0.05 -> 5 degrees in resolution
ticks = np.logspace(np.log10(0.05), np.log10(5), num=19)
areas_50 = diameter_to_steradian(ticks, 0.5) * (180./np.pi)**2 
areas_90 = diameter_to_steradian(ticks, 0.9) * (180./np.pi)**2
for tick, a50, a90 in zip(ticks, areas_50, areas_90):
	print("Resolution {:.2f}, 50% {:.4f}, 90% {:.4f}".format(tick, a50, a90))


fig = plt.figure(figsize=(5,2))
ax = fig.add_subplot(111)
ax.scatter(areas_90, np.zeros_like(areas_90))
ax.set_xlim([areas_90[0], areas_90[-1]])
ax.set_xscale('log')
ax.get_yaxis().set_ticks([])
ax.tick_params(axis='x', labelsize=12)
ax.set_xlabel(r'90% containment area on the sky [deg$^2$]',size=14)
plt.tight_layout()
fig.savefig("axis_90.png", dpi=300)