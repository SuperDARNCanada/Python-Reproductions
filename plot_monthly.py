# (C) SuperDARN Canada University of Saskatchewan 
# Plots time series of echo counts, see --help for more info

import numpy as np
import argparse
from calendar import monthrange
import collections
from datetime import datetime as dt
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.dates as mdates
import matplotlib

# Below two lines allow interaction with the terminal
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def monthly_plotN(year, month, rgates):
	# Preallocate counts variables
	gs_count = 0
	gs_frac = 0
	is_count = 0
	is_frac = 0
	mth_fill = str(month).zfill(2)
	# Load each respective column from preexisting text files
	day = np.loadtxt('/home/kehler/Python-Reproductions/{}/nh_{}_{}{}'.format(year, rgates[0], year, mth_fill))[:,2]
	hr = np.loadtxt('/home/kehler/Python-Reproductions/{}/nh_{}_{}{}'.format(year, rgates[0], year, mth_fill))[:,3]
	num_rdrs = np.loadtxt('/home/kehler/Python-Reproductions/{}/nh_{}_{}{}'.format(year, rgates[0], year, mth_fill))[:,9]
	time_array = np.zeros(len(day), dtype='datetime64[h]')

	# Loop through list of range gates and sum their counts arrays
	for rgs in rgates:
		gs_count += np.loadtxt('/home/kehler/Python-Reproductions/{}/nh_{}_{}{}'.format(year, rgs, year, mth_fill))[:,4]
		is_count += np.loadtxt('/home/kehler/Python-Reproductions/{}/nh_{}_{}{}'.format(year, rgs, year, mth_fill))[:,5]
		gs_frac += np.loadtxt('/home/kehler/Python-Reproductions/{}/nh_{}_{}{}'.format(year, rgs, year, mth_fill))[:,7]
		is_frac += np.loadtxt('/home/kehler/Python-Reproductions/{}/nh_{}_{}{}'.format(year, rgs, year, mth_fill))[:,8]

	# Convert times to integers
	day = day.astype(int)
	hr = hr.astype(int)

	# Convert to datetime objects
	for i, (d, h) in enumerate(zip(day, hr)):
		time_array[i] = dt(year, month, d, h)

	dates = time_array.astype('O')
	mth_name = dt.strftime(dt(year,month,1), '%B')

	fig, ax = plt.subplots(figsize=(15,6))
	ax.plot(dates, gs_count)
	ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
	plt.title('Echos vs Time - North ' + mth_name + ' , ' + str(year))
	plt.xlabel('Time')
	plt.ylabel('Ground Echo Counts')
	# plt.savefig('/home/kehler/Python-Reproductions/EchoPlots/EPlots_{}{}/GSechosS_{}.jpg'.format(gts[:4], rgates[-1][-2:], year))

	fig, ax = plt.subplots(figsize=(15,6))
	ax.plot(dates, is_count)
	ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
	plt.title('Echos vs Time - North ' + mth_name + ' , ' + str(year))
	plt.xlabel('Time')
	plt.ylabel('Ionospheric Echo Counts')
	# plt.savefig('/home/kehler/Python-Reproductions/EchoPlots/EPlots_{}{}/ISechosS_{}.jpg'.format(gts[:4], rgates[-1][-2:], year))
	
	plt.show(block=True)


def monthly_plotS(year, month, rgates):
	# Preallocate counts variables
	gs_count = 0
	gs_frac = 0
	is_count = 0
	is_frac = 0
	mth_fill = str(month).zfill(2)
	# Load each respective column from preexisting text files
	day = np.loadtxt('/home/kehler/Python-Reproductions/{}/sh_{}_{}{}'.format(year, rgates[0], year, mth_fill))[:,2]
	hr = np.loadtxt('/home/kehler/Python-Reproductions/{}/sh_{}_{}{}'.format(year, rgates[0], year, mth_fill))[:,3]
	num_rdrs = np.loadtxt('/home/kehler/Python-Reproductions/{}/sh_{}_{}{}'.format(year, rgates[0], year, mth_fill))[:,9]
	time_array = np.zeros(len(day), dtype='datetime64[h]')

	# Loop through list of range gates and sum their counts arrays
	for rgs in rgates:
		gs_count += np.loadtxt('/home/kehler/Python-Reproductions/{}/sh_{}_{}{}'.format(year, rgs, year, mth_fill))[:,4]
		is_count += np.loadtxt('/home/kehler/Python-Reproductions/{}/sh_{}_{}{}'.format(year, rgs, year, mth_fill))[:,5]
		gs_frac += np.loadtxt('/home/kehler/Python-Reproductions/{}/sh_{}_{}{}'.format(year, rgs, year, mth_fill))[:,7]
		is_frac += np.loadtxt('/home/kehler/Python-Reproductions/{}/sh_{}_{}{}'.format(year, rgs, year, mth_fill))[:,8]

	# Convert times to integers
	day = day.astype(int)
	hr = hr.astype(int)

	# Convert to datetime objects
	for i, (d, h) in enumerate(zip(day, hr)):
		time_array[i] = dt(year, month, d, h)

	dates = time_array.astype('O')
	mth_name = dt.strftime(dt(year,month,1), '%B')

	fig, ax = plt.subplots(figsize=(15,6))
	ax.plot(dates, gs_count)
	ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
	plt.title('Echos vs Time - South ' + mth_name + ' , ' + str(year))
	plt.xlabel('Time')
	plt.ylabel('Ground Echo Counts')
	# plt.savefig('/home/kehler/Python-Reproductions/EchoPlots/EPlots_{}{}/GSechosS_{}.jpg'.format(gts[:4], rgates[-1][-2:], year))

	fig, ax = plt.subplots(figsize=(15,6))
	ax.plot(dates, is_count)
	ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
	plt.title('Echos vs Time - South ' + mth_name + ' , ' + str(year))
	plt.xlabel('Time')
	plt.ylabel('Ionospheric Echo Counts')
	# plt.savefig('/home/kehler/Python-Reproductions/EchoPlots/EPlots_{}{}/ISechosS_{}.jpg'.format(gts[:4], rgates[-1][-2:], year))
	
	plt.show(block=True)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Creates monthly time series of echo counts from ground and ionosphere')
	parser.add_argument('year', type=int, help='The year of data you wish to plot')
	parser.add_argument('range_gates', nargs='+', help='The range(s) of rangegates you wish to use; options are: [00,16,33,49] to [15,32,48,64]')
	parser.add_argument('month', type=int, help='The month you wish to plot')
	args = parser.parse_args()
	year = args.year
	gates = args.range_gates
	month = args.month

	monthly_plotN(year, month, gates)
	monthly_plotS(year, month, gates)