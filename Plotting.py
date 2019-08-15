# Plots time series of echo counts for the Northern Hemisphere
import numpy as np
import os, sys
from calendar import monthrange
import collections
from datetime import datetime as dt
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.dates as mdates
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def plot_echos_N(year, rgates):
	# Load each respective column from preexisting text files
	yr = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/nh_{}_{}'.format(rgates, rgates, year))[:,0]
	mth = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/nh_{}_{}'.format(rgates, rgates, year))[:,1]
	day = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/nh_{}_{}'.format(rgates, rgates, year))[:,2]
	hr = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/nh_{}_{}'.format(rgates, rgates, year))[:,3]
	gs_count = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/nh_{}_{}'.format(rgates, rgates, year))[:,4]
	is_count = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/nh_{}_{}'.format(rgates, rgates, year))[:,5]
	total_count = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/nh_{}_{}'.format(rgates, rgates, year))[:,6]
	gs_frac = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/nh_{}_{}'.format(rgates, rgates, year))[:,7]
	is_frac = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/nh_{}_{}'.format(rgates, rgates, year))[:,8]
	num_rdrs = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/nh_{}_{}'.format(rgates, rgates, year))[:,9]
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
	print len(dates), len(is_count), len(gs_count)

	plt.figure(1)
	plt.plot(dates, gs_count/num_rdrs)
	plt.title('Echos vs Time - North ' + str(yr[0]))
	plt.xlabel('Time')
	plt.ylabel('Ground Echo Counts per Radar')
	plt.savefig('/home/kehler/Python-Reproductions/EchoPlots/EPlots_{}/GSechosN_{}.jpg'.format(rgates, year))

	plt.figure(2)
	plt.plot(dates, is_count/num_rdrs)
	plt.title('Echos vs Time - North ' + str(yr[0]))
	plt.xlabel('Time')
	plt.ylabel('Ionospheric Echo Counts per Radar')
	plt.savefig('/home/kehler/Python-Reproductions/EchoPlots/EPlots_{}/ISechosN_{}.jpg'.format(rgates, year))
	

	plt.show(block=True)


def plot_echos_S(year, rgates):
	# Load each respective column from preexisting text files
	yr = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/sh_{}_{}'.format(rgates, rgates, year))[:,0]
	mth = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/sh_{}_{}'.format(rgates, rgates, year))[:,1]
	day = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/sh_{}_{}'.format(rgates, rgates, year))[:,2]
	hr = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/sh_{}_{}'.format(rgates, rgates, year))[:,3]
	gs_count = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/sh_{}_{}'.format(rgates, rgates, year))[:,4]
	is_count = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/sh_{}_{}'.format(rgates, rgates, year))[:,5]
	total_count = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/sh_{}_{}'.format(rgates, rgates, year))[:,6]
	gs_frac = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/sh_{}_{}'.format(rgates, rgates, year))[:,7]
	is_frac = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/sh_{}_{}'.format(rgates, rgates, year))[:,8]
	num_rdrs = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/sh_{}_{}'.format(rgates, rgates, year))[:,9]
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
	plt.plot(dates, gs_count/num_rdrs)
	plt.title('Echos vs Time - South ' + str(yr[0]))
	plt.xlabel('Time')
	plt.ylabel('Ground Echo Counts per Radar')
	plt.savefig('/home/kehler/Python-Reproductions/EchoPlots/EPlots_{}/GSechosS_{}.jpg'.format(rgates, year))

	plt.figure(2)
	plt.plot(dates, is_count/num_rdrs)
	plt.title('Echos vs Time - South ' + str(yr[0]))
	plt.xlabel('Time')
	plt.ylabel('Ionospheric Echo Counts per Radar')
	plt.savefig('/home/kehler/Python-Reproductions/EchoPlots/EPlots_{}/ISechosS_{}.jpg'.format(rgates, year))
	
	plt.show(block=True)


def totals_yearly(year):
	gs_count_n = 0
	gs_count_s = 0
	is_count_n = 0
	is_count_s = 0

	for rgates in ['0to15', '16to32', '33to48', '49to64']:
		print (year, rgates, np.size(gs_count_s))
		# Northern Files
		gs_count_n += np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/nh_{}_{}'.format(rgates, rgates, year))[:,4]
		is_count_n += np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/nh_{}_{}'.format(rgates, rgates, year))[:,5]
		
		# Southern Files
		gs_count_s += np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/sh_{}_{}'.format(rgates, rgates, year))[:,4]
		is_count_s += np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/sh_{}_{}'.format(rgates, rgates, year))[:,5]
	
	gs_n = np.sum(gs_count_n)
	gs_s = np.sum(gs_count_s)
	is_n = np.sum(is_count_n)
	is_s = np.sum(is_count_s)

	return (gs_n, gs_s, is_n, is_s)


def totals_yearly_per_radar(year):
	print 'per radar'
	gs_count_n = 0
	gs_count_s = 0
	is_count_n = 0
	is_count_s = 0

	for rgates in ['0to15', '16to32', '33to48', '49to64']:
		# Northern Files
		gs_count_n += np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/nh_{}_{}'.format(rgates, rgates, year))[:,4]
		is_count_n += np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/nh_{}_{}'.format(rgates, rgates, year))[:,5]
		
		# Southern Files
		gs_count_s += np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/sh_{}_{}'.format(rgates, rgates, year))[:,4]
		is_count_s += np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/sh_{}_{}'.format(rgates, rgates, year))[:,5]
		

	num_rdrs_n = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/nh_{}_{}'.format('16to32', '16to32', year))[:,9]
	num_rdrs_s = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/sh_{}_{}'.format('16to32', '16to32', year))[:,9]

	gs_total_n = gs_count_n/num_rdrs_n
	is_total_n = is_count_n/num_rdrs_n
	gs_total_s = gs_count_s/num_rdrs_s
	is_total_s = is_count_s/num_rdrs_s

	gs_per_rdr_n = np.nansum(gs_total_n)
	gs_per_rdr_s = np.nansum(gs_total_s)
	is_per_rdr_n = np.nansum(is_total_n)
	is_per_rdr_s = np.nansum(is_total_s)

	return (gs_per_rdr_n, gs_per_rdr_s, is_per_rdr_n, is_per_rdr_s)


def plot_num_rdrs(rgates):
	rdrs_n_daily = []
	rdrs_s_daily = []
	time_array = []

	for year in range(2007, 2020):
		num_rdrs_n = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/nh_{}_{}'.format(rgates, rgates, year))[:,9].tolist()
		num_rdrs_s = np.loadtxt('/home/kehler/Python-Reproductions/RG_{}/sh_{}_{}'.format(rgates, rgates, year))[:,9].tolist()

		rdrs_n_daily += num_rdrs_n[0::24]
		rdrs_s_daily += num_rdrs_s[0::24]

	date = dt(2007, 1, 1)
	enddate = dt(2019, 4, 27)
	while date <= enddate:
		time_array.append(date)
		date += relativedelta(days=1)

	time_arr = np.array(time_array).astype('O')
	plt.figure(1)
	ax1 = plt.subplot(211)
	plt.plot(time_arr, rdrs_n_daily)	
	plt.title('Number of Radars per Day: North')
	plt.setp(ax1.get_xticklabels(), visible=False)
	plt.ylabel('Num Rdrs')

	ax2 = plt.subplot(212, sharex=ax1)
	plt.plot(time_arr, rdrs_s_daily)
	plt.title('Number of Radars per Day: South')
	plt.ylabel('Num Rdrs')
	plt.xlabel('Time, [days]')

	plt.tight_layout()
	plt.show()


def plot_yearly_counts():
	gs_North = []
	gs_South = []
	is_North = []
	is_South = []

	gs_per_rdr_North = []
	gs_per_rdr_South = []
	is_per_rdr_North = []
	is_per_rdr_South = []

	for year in range(2007,2020):
		gN, gS, iN, iS = totals_yearly(year)
		grn, grs, irn, irs = totals_yearly_per_radar(year)
		gs_North.append(gN)
		gs_South.append(gS)
		is_North.append(iN)
		is_South.append(iS)
		gs_per_rdr_North.append(grn)
		gs_per_rdr_South.append(grs)
		is_per_rdr_North.append(irn)
		is_per_rdr_South.append(irs)

	time_array = np.arange(2007, 2020)

	plt.figure(1)
	ax1 = plt.subplot(411)
	plt.plot(time_array, gs_North)	
	plt.title('Ground Scatter Counts: North')
	plt.setp(ax1.get_xticklabels(), visible=False)
	plt.ylabel('counts')

	ax2 = plt.subplot(412, sharex=ax1)
	plt.plot(time_array, gs_South)
	plt.title('Ground Scatter Counts: South')
	plt.setp(ax2.get_xticklabels(), visible=False)
	plt.ylabel('counts')

	ax3 = plt.subplot(413, sharex=ax1)
	plt.plot(time_array, is_North)
	plt.title('Ionosperic Scatter Counts: North')
	plt.setp(ax3.get_xticklabels(), visible=False)
	plt.ylabel('counts')

	ax4 = plt.subplot(414, sharex=ax1)
	plt.plot(time_array, is_South)
	plt.title('Ionospheric Scatter Counts: South')
	plt.xlabel('Time, [yr]')
	plt.ylabel('counts')

	plt.tight_layout()

	plt.figure(2)
	ax1 = plt.subplot(411)
	plt.plot(time_array, gs_per_rdr_North)	
	plt.title('Ground Scatter Counts per Radar: North')
	plt.setp(ax1.get_xticklabels(), visible=False)
	plt.ylabel('cnts/rdr')
	
	ax2 = plt.subplot(412, sharex=ax1)
	plt.plot(time_array, gs_per_rdr_South)
	plt.title('Ground Scatter Counts per Radar: South')
	plt.setp(ax2.get_xticklabels(), visible=False)
	plt.ylabel('cnts/rdr')

	ax3 = plt.subplot(413, sharex=ax1)
	plt.plot(time_array, is_per_rdr_North)
	plt.title('Ionospheric Scatter Counts per Radar: North')
	plt.setp(ax3.get_xticklabels(), visible=False)
	plt.ylabel('cnts/rdr')

	ax4 = plt.subplot(414, sharex=ax1)
	plt.plot(time_array, is_per_rdr_South)
	plt.title('Ionospheric Scatter Counts per Radar: South')
	plt.xlabel('Time, [yr]')
	plt.ylabel('cnts/rdr')
	
	plt.tight_layout()
	plt.show()


if __name__ == '__main__':
	year = sys.argv[1]
	rgates = sys.argv[2]
	plot_echos_N(year, rgates)
	plot_echos_S(year, rgates)
	# plot_yearly_counts()
	# plot_num_rdrs('16to32')
