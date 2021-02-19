import matplotlib.pyplot as plt
import sys
import numpy as np
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
import astropy.coordinates as coord
from astropy.io import ascii
import pandas as pd
import yaml
import itertools
from astropy.io import fits

def get_lac():

	fits_lac = fits.open('data/table_4LAC.fits')
	data = fits_lac[1].data

	source_ra = data.field('RAJ2000')
	source_dec = data.field('DEJ2000')
	source_class = data.field('CLASS')
	source_flux = data.field('Flux1000')
	source_energyflux = data.field('Energy_Flux100')

	return source_ra, source_dec, source_class, source_flux, source_energyflux


# Read data and convert to desired coordinates

galactic_longitudes = np.arange(start=0, stop=360, step=0.1)
galactic_latitudes = [0] * len(galactic_longitudes)
icrs = SkyCoord(galactic_longitudes, galactic_latitudes, unit="deg", frame="galactic").icrs
gal_ra = icrs.ra
gal_ra = gal_ra.wrap_at(180*u.degree)
gal_dec = icrs.dec


gal_center_long = 180.
gal_center_lat = 0.
cena_long = 309.51589568
cena_lat = 19.41727350
icrs2 = SkyCoord(gal_center_long, gal_center_lat, unit="deg", frame="galactic").icrs
gal_center_ra = icrs2.ra
gal_center_ra = gal_center_ra.wrap_at(180*u.degree)
gal_center_dec = icrs2.dec


icrs3 = SkyCoord(cena_long, cena_lat, unit="deg", frame="galactic").icrs

ra_gc=299.3*u.degree
dec_gc=-28.72* u.degree
ra_cena = 201.3625*u.degree
dec_cena = -43.0192*u.degree
c2 = SkyCoord(ra=ra_cena, dec=dec_cena, frame='icrs')
cena_ra = c2.ra.wrap_at(180 * u.deg).radian
cena_dec = c2.dec.radian

ra_txs = 77.3582*u.degree
dec_txs = 5.69314*u.degree
c3 = SkyCoord(ra=ra_txs, dec=dec_txs, frame='icrs')
txs_ra = c3.ra.wrap_at(180 * u.deg).radian
txs_dec = c3.dec.radian


def convertCoord(RA, Dec):
    ra = coord.Angle(RA*u.degree)
    ra = ra.wrap_at(180*u.degree)
    dec = coord.Angle(Dec*u.degree)
    c2 = SkyCoord(ra=ra, dec=dec, frame='icrs')
    ra_rad = c2.ra.wrap_at(180 * u.deg).radian
    dec_rad = c2.dec.radian
    return ra_rad, dec_rad


# ### UHECR catalog from Rachen and Eichmann (https://arxiv.org/abs/1909.00261)
UHECR = pd.read_csv("data/UHECR_catalog.csv")
UHECR.head()


c = SkyCoord(ra=ra_gc, dec=dec_gc, frame='icrs')
fig = plt.figure(figsize=(10,6.5))
ax = fig.add_subplot(111, projection="mollweide")
ra_rad = c.ra.wrap_at(180 * u.deg).radian
dec_rad = c.dec.radian
ax.grid(color='k', linestyle='solid', linewidth=0.5)
r = 90
#theta = np.arange(0,2*np.pi,0.1)
x = np.array([-np.pi,np.pi,np.pi,-np.pi,-np.pi])
y2 = np.array([0.05,0.05,-0.82,-0.82,0.05])

plt.fill(x,y2,label='200m deep station FOV', facecolor='grey',alpha=0.2)
# plt.plot(ra_rad, dec_rad, '*',color='gold',markersize=20,mec='firebrick',label='Galactic Center')
plt.plot(ra_rad, dec_rad, '*',color='black',markersize=15,mec='black')
plt.plot(gal_ra.radian[0:2970], -gal_dec.radian[0:2970],color='black',linewidth=2,label='Galactic Plane and Center',zorder=1)
plt.plot(gal_ra.radian[2980:], -gal_dec.radian[2980:],color='black',linewidth=2,zorder=2)
marker = itertools.cycle(('>', '+', '<', 'o', '*', 'X')) 

num_points_plotted=0
for index, source in UHECR.iterrows():
#     print(source['RA'], source['Dec'])    
    ra_source, dec_source = convertCoord(source['RA'], source['DEC'])
    if(dec_source>0.05 or dec_source<-0.82): continue
    if num_points_plotted==0:
        ax.plot(ra_source, dec_source,'x', color='C0', mew=2,markersize=10, label='Radio-loud AGN (Rachen \'19)')
        num_points_plotted+=1
    else:
        ax.plot(ra_source, dec_source,'kx',color='C0',mew=2,markersize=10)

lac_ra, lac_dec, source_class, flux, e_flux = get_lac()

# sort out which sources to plot
e_flux = np.asarray(e_flux)
e_flux_sorted = np.sort(e_flux)[::-1] # sort and return in descending order
cut = e_flux_sorted[100]

lac_ra, lac_dec = convertCoord(lac_ra, -lac_dec)
lac_ra = np.asarray(lac_ra)
lac_dec = np.asarray(lac_dec)
lac_plot_ra = []
lac_plot_dec = []
unique_types = np.unique(source_class)
for i in range(len(lac_ra)):
	this_ra = lac_ra[i]
	this_dec = lac_dec[i]
	this_source = source_class[i]
	this_eflux = e_flux[i]
	if this_dec >-0.82 and this_dec < 0.05:
	# if 1==1:
		if this_source not in ['rdg', 'RDG', 'SSRQ', 'ssrq', 'nlsy1', 'NLSY1', 'css']:
			if this_eflux >= cut:
				lac_plot_ra.append(this_ra)
				lac_plot_dec.append(this_dec)

ax.plot(lac_plot_ra,lac_plot_dec, 'C2+', mew=2, markersize=12, label='Bright 4LAC Blazars')


legend = ax.legend()
legend.get_frame().set_facecolor('#ffe4c4')
plt.legend(ncol=1,loc=(0.51,0.65), fontsize=15, framealpha=1)
ax.set_ylabel('Declination (deg)', fontsize=15) #give it a title
ax.set_xlabel('Right Ascension (deg)',labelpad=20, fontsize=15) #give it a title
ax.tick_params(direction='out', length=8, width=4, colors='k',
               grid_color='k', grid_alpha=0.2, labelsize=13, grid_linewidth=1)
ax.axes.get_xaxis().set_ticks([-np.pi/3, -2*np.pi/3, -np.pi,0,np.pi/3, 2*np.pi/3, np.pi])
# plt.gca().set_aspect('0.9', adjustable='box')
# plt.suptitle("Radio galaxies as UHECR sources \n Rachen & Eichmann",fontsize=20)

# Cen A
ax.plot(cena_ra, cena_dec,'d',markersize=10,color='C3')
# Centaurus A∗,201.37,-43.02,300,4,FR-I
ax.annotate(r'Cen A', xy=(cena_ra*1.135,1.28*cena_dec), xycoords='data',
	size=15, color='C3')

# TXS
ax.plot(txs_ra, txs_dec,'d',markersize=10,color='C3')
# Centaurus A∗,201.37,-43.02,300,4,FR-I
ax.annotate(r'TXS 0506', xy=(txs_ra*0.87,1.60*txs_dec), xycoords='data',
	size=15, color='C3')

plt.tight_layout()
plt.savefig("gen2_fov_w_uhecr_4lac.png", dpi=300)

print('Got here')


