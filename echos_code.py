# (C) SuperDARN Canada University of Saskatchewan 
# This script contains multiple functions necessary for the calculation of the number of ground 
# and ionospheric echos in a given day. This code is callable through GNU parallel to obtain
# calculations for a range of days. As a result, this script requires one input value, in the
# format of a date string - yyyymmdd

# Note that the format of the file reading assumes that there is only one file type for a given
# radar on the chosen day. ie: if there is both a .gz and .bz2, it will open both.

import backscatter.dmap.dmap as dm
from backscatter.dmap.dmap import DmapDataError
from backscatter.dmap.dmap import EmptyFileError
import numpy as np
import fnmatch
import os, sys
import gzip
import bz2
from calendar import monthrange
import collections
import time	

def counts_calcs(records, min_idx, max_idx, list_hrs, i, gs_count, is_count):
	hr = records[i]['time.hr']
	list_hrs.append(hr)
	
	try:
		index = np.where((records[i]['slist'] > min_idx) & (records[i]['slist'] < max_idx))[0]
		ranges = [records[i]['slist'][x] for x in index]
		gflg = np.array([records[i]['gflg'][x] for x in index])

		gs_count[hr] += np.count_nonzero(gflg)
		pwr = [records[i]['pwr0'][x] for x in ranges]

		inx = np.where(gflg == 0)[0]
		is_count[hr] += np.count_nonzero([pwr[x] > 3. for x in inx])
	except:
		pass
	return (gs_count, is_count, list_hrs)


def total_calcs(list_hrs, num_gates, num_cnts_poss):
	start = time.time()
	counter = collections.Counter(list_hrs)
	num_poss_rdr = [x*num_gates for x in counter.values()]

	try:
		num_cnts_poss = [num_cnts_poss[x] + num_poss_rdr[x] for x in range(24)]
	except:
		missing_hrs = [x for x in range(24) if x not in counter.keys()]
		[num_poss_rdr.insert(x,0) for x in missing_hrs]
		num_cnts_poss = [num_cnts_poss[x] + num_poss_rdr[x] for x in range(24)]
	end = time.time()
	print 'All possible counts calculations took ' + str(end-start) + ' seconds'
	return num_cnts_poss


def write_to_file(gs_count_n, is_count_n, gs_count_s, is_count_s, num_cnts_poss_n, num_cnts_poss_s, yr, mth, day, num_radars_north, num_radars_south, name):
	start_pop = time.time()
	with open('nh_' + name + '_' + str(date), 'a') as north, open('sh_' + name + '_' + str(date), 'a') as south:
		for hr in range(24):
			gs_frac_n = gs_count_n[hr]/num_cnts_poss_n[hr]
			is_frac_n = is_count_n[hr]/num_cnts_poss_n[hr]
			gs_frac_s = gs_count_s[hr]/num_cnts_poss_s[hr]
			is_frac_s = is_count_s[hr]/num_cnts_poss_s[hr]
			
			north.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(yr, mth, day, hr, gs_count_n[hr], is_count_n[hr], num_cnts_poss_n[hr], gs_frac_n, is_frac_n, num_radars_north))
			south.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(yr, mth, day, hr, gs_count_s[hr], is_count_s[hr], num_cnts_poss_s[hr], gs_frac_s, is_frac_s, num_radars_south))
	end_pop = time.time()
	print 'Writing took ' + str(end_pop-start_pop) + ' seconds'


def calc_counts_daily(date):
	yr = str(date)[:4]
	mth = str(date)[4:6]
	day = str(date)[6:8]
	north_st_ids = [209, 208, 33, 207, 206, 66, 205, 204, 1, 10, 40, 41, 64, 3, 16, 7, 90, 9, 6, 65, 5, 8, 32]
	south_st_ids = [24, 96, 21, 4, 15, 20, 11, 22, 13, 12, 14, 18, 19]

	num_radars_north = 0
	num_radars_south = 0
	ncp_n1, ncp_n2, ncp_n3, ncp_n4 = [0]*24, [0]*24, [0]*24, [0]*24
	ncp_s1, ncp_s2, ncp_s3, ncp_s4 = [0]*24, [0]*24, [0]*24, [0]*24
	gscN_1, gscN_2, gscN_3, gscN_4 = np.zeros(24), np.zeros(24), np.zeros(24), np.zeros(24)
	iscN_1, iscN_2, iscN_3, iscN_4 = np.zeros(24), np.zeros(24), np.zeros(24), np.zeros(24)
	gscS_1, gscS_2, gscS_3, gscS_4 = np.zeros(24), np.zeros(24), np.zeros(24), np.zeros(24)
	iscS_1, iscS_2, iscS_3, iscS_4 = np.zeros(24), np.zeros(24), np.zeros(24), np.zeros(24)

	filepath = '/data/fitcon/' + yr + '/' + mth + '/'
	file_string = sorted(np.array(os.listdir(filepath)))
	filtered = fnmatch.filter(file_string, str(date) + '.*')
	fitfiles = [filepath + x for x in filtered]
	good_files = np.where(np.array(fitfiles) != '/data/fitcon/2007/01/20070117.C0.han.fitacf.gz')
	fitfiles = np.array(fitfiles)[good_files]

	print 'starting for loop through files'
	start_for = time.time()
	for file in fitfiles:
		print 'The file is:', file
		start = time.time()

		print 'trying to open the file'
		try:
			if '.gz' in file:
				with gzip.open(file, 'r') as f:
					raw_data = f.read()
				records = dm.parse_dmap_format_from_stream(raw_data)
			elif '.bz2' in file:
				with bz2.BZ2File(file, 'r') as f:
					raw_data = f.read()
				records = dm.parse_dmap_format_from_stream(raw_data)
			else:
				records = dm.parse_dmap_format_from_file(file)
			end = time.time()
			print 'Opening file ' + str(file) + ' took ' + str(end-start) + ' seconds'
		except EOFError as err:
			with open('errors_list', 'a') as f:
				f.write('{}\t{}\n'.format(file, err))
			print 'logged EOFError'
			end = time.time()
			# print 'error log took ' + str(end-start) + ' seconds'
			continue
		except DmapDataError as err:
			with open('errors_list', 'a') as f:
				f.write('{}\t{}\n'.format(file, err))
			print 'logged corrupt file error'
			end = time.time()
			# print 'error log took ' + str(end-start) + ' seconds'
			continue
		except EmptyFileError as err:
			with open('errors_list', 'a') as f:
				f.write('{}\t{}\n'.format(file, err))
			print 'logged data stream error'
			end = time.time()
			# print 'error log took ' + str(end-start) + ' seconds'
			continue
		except:
			with open('errors_list', 'a') as f:
				f.write('{}\t{}\n'.format(file, 'unknown error'))
			print 'logged some other error'
			end = time.time()
			# print 'error log took ' + str(end-start) + ' seconds'
			continue

		num_gates = 16
		# select data for range gates 0-15
		
		if records[0]['stid'] in north_st_ids:
			num_radars_north += 1
			hrs_1, hrs_2, hrs_3, hrs_4 = [], [], [], []

			print 'Begin loop through records'
			start = time.time()
			for i in range(len(records)):
				# gscN_1, iscN_1, hrs_1 = counts_calcs(records, 16, 33, hrs_1, i, gscN_1, iscN_1)
				gscN_2, iscN_2, hrs_2 = counts_calcs(records, 32, 49, hrs_2, i, gscN_2, iscN_2)
				gscN_3, iscN_3, hrs_3 = counts_calcs(records, 48, 65, hrs_3, i, gscN_3, iscN_3)
				# gscN_4, iscN_4, hrs_4 = counts_calcs(records, 0, 16, hrs_4, i, gscN_4, iscN_4)
			end = time.time()
			print 'Total records looping time is ' + str(end-start) + ' seconds'

			# Create the list of # records per hour for this radar times the number of gates, this is 
			# possible counts for this radar per hour
			# ncp_n1 = total_calcs(hrs_1, num_gates, ncp_n1)
			ncp_n2 = total_calcs(hrs_2, num_gates, ncp_n2)
			ncp_n3 = total_calcs(hrs_3, num_gates, ncp_n3)
			# ncp_n4 = total_calcs(hrs_4, num_gates, ncp_n4)

		else:
			num_radars_south += 1
			hrs_1, hrs_2, hrs_3, hrs_4 = [], [], [], []

			print 'Begin loop through records'
			start = time.time()
			for i in range(len(records)):
				# gscS_1, iscS_1, hrs_1 = counts_calcs(records, 16, 33, hrs_1, i, gscS_1, iscS_1)
				gscS_2, iscS_2, hrs_2 = counts_calcs(records, 32, 49, hrs_2, i, gscS_2, iscS_2)
				gscS_3, iscS_3, hrs_3 = counts_calcs(records, 48, 65, hrs_3, i, gscS_3, iscS_3)
				# gscS_4, iscS_4, hrs_4 = counts_calcs(records, 0, 16, hrs_4, i, gscS_4, iscS_4)
			end = time.time()
			print 'Total records looping time is ' + str(end-start) + ' seconds'

			# ncp_s1 = total_calcs(hrs_1, num_gates, ncp_s1)
			ncp_s2 = total_calcs(hrs_2, num_gates, ncp_s2)
			ncp_s3 = total_calcs(hrs_3, num_gates, ncp_s3)
			# ncp_s4 = total_calcs(hrs_4, num_gates, ncp_s4)

	end_for = time.time()
	print 'Looping through files took ' + str(end_for - start_for) + ' seconds'
	print 'Starting file population'
	
	# write_to_file(gscN_1, iscN_1, gscS_1, iscS_1, ncp_n1, ncp_s1, yr, mth, day, num_radars_north, num_radars_south, '16to32')
	write_to_file(gscN_2, iscN_2, gscS_2, iscS_2, ncp_n2, ncp_s2, yr, mth, day, num_radars_north, num_radars_south, 't33to48')
	write_to_file(gscN_3, iscN_3, gscS_3, iscS_3, ncp_n3, ncp_s3, yr, mth, day, num_radars_north, num_radars_south, 't49to64')
	# write_to_file(gscN_4, iscN_4, gscS_4, iscS_4, ncp_n4, ncp_s4, yr, mth, day, num_radars_north, num_radars_south, '0to15')

if __name__ == '__main__':
	date = sys.argv[1]
	print 'Starting calculations for this day'
	start_day = time.time()
	calc_counts_daily(date)	
	end_day = time.time()		
	print 'Done! This day took ' + str(end_day-start_day) + ' seconds'