# Plots time series of echo counts for the Northern Hemisphere

import numpy as np
import os, sys
from calendar import monthrange
import collections
from datetime import datetime as dt
import matplotlib.dates as mdates
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def plot_echos_N(year):
	# Load each respective column from preexisting text files
	yr = np.loadtxt('nh_first15_{}'.format(year))[:,0]
	mth = np.loadtxt('nh_first15_{}'.format(year))[:,1]
	day = np.loadtxt('nh_first15_{}'.format(year))[:,2]
	hr = np.loadtxt('nh_first15_{}'.format(year))[:,3]
	gs_count = np.loadtxt('nh_first15_{}'.format(year))[:,4]
	is_count = np.loadtxt('nh_first15_{}'.format(year))[:,5]
	total_count = np.loadtxt('nh_first15_{}'.format(year))[:,6]
	gs_frac = np.loadtxt('nh_first15_{}'.format(year))[:,7]
	is_frac = np.loadtxt('nh_first15_{}'.format(year))[:,8]
	num_rdrs = np.loadtxt('nh_first15_{}'.format(year))[:,9]
	time_array = np.zeros(len(yr), dtype='datetime64[h]')

	# Convert times to integers
	yr = yr.astype(int)
	mth = mth.astype(int)
	day = day.astype(int)
	hr = hr.astype(int)

	# Convert to datetime objects
	for i, (m, d, h) in enumerate(zip(mth, day, hr)):
		time_array[i] = dt(yr[0], m, d, h)

	dates = time_array.astype('O')
	plt.figure(1)
	plt.plot(dates, gs_count)
	plt.title('Echos vs Time - North ' + str(yr[0]))
	plt.xlabel('Time')
	plt.ylabel('Ground Echo Counts')
	plt.savefig('GSechosN_{}.jpg'.format(year))

	plt.figure(2)
	plt.plot(dates, is_count)
	plt.title('Echos vs Time - North ' + str(yr[0]))
	plt.xlabel('Time')
	plt.ylabel('Ionospheric Echo Counts')
	plt.savefig('ISechosN_{}.jpg'.format(year))
	
	plt.show(block=True)


def plot_echos_S(year):
	# Load each respective column from preexisting text files
	yr = np.loadtxt('sh_first15_{}'.format(year))[:,0]
	mth = np.loadtxt('sh_first15_{}'.format(year))[:,1]
	day = np.loadtxt('sh_first15_{}'.format(year))[:,2]
	hr = np.loadtxt('sh_first15_{}'.format(year))[:,3]
	gs_count = np.loadtxt('sh_first15_{}'.format(year))[:,4]
	is_count = np.loadtxt('sh_first15_{}'.format(year))[:,5]
	total_count = np.loadtxt('sh_first15_{}'.format(year))[:,6]
	gs_frac = np.loadtxt('sh_first15_{}'.format(year))[:,7]
	is_frac = np.loadtxt('sh_first15_{}'.format(year))[:,8]
	num_rdrs = np.loadtxt('sh_first15_{}'.format(year))[:,9]
	time_array = np.zeros(len(yr), dtype='datetime64[h]')

	# Convert times to integers
	yr = yr.astype(int)
	mth = mth.astype(int)
	day = day.astype(int)
	hr = hr.astype(int)

	# Convert to datetime objects
	for i, (m, d, h) in enumerate(zip(mth, day, hr)):
		time_array[i] = dt(yr[0], m, d, h)

	dates = time_array.astype('O')
	plt.figure(1)
	plt.plot(dates, gs_count)
	plt.title('Echos vs Time - South ' + str(yr[0]))
	plt.xlabel('Time')
	plt.ylabel('Ground Echo Counts')
	plt.savefig('GSechosS_{}.jpg'.format(year))

	plt.figure(2)
	plt.plot(dates, is_count)
	plt.title('Echos vs Time - South ' + str(yr[0]))
	plt.xlabel('Time')
	plt.ylabel('Ionospheric Echo Counts')
	plt.savefig('ISechosS_{}.jpg'.format(year))
	
	plt.show(block=True)


if __name__ == '__main__':
	year = sys.argv[1]
	plot_echos_N(year)
	plot_echos_S(year)