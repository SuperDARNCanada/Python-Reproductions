# Calculates the ground and ionospheric echos per hour from all radars, north and south
# separately, through a specified number of range gates
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

def calc_counts_daily(date):
	yr = str(date)[:4]
	mth = str(date)[4:6]
	day = str(date)[6:8]
	north_st_ids = [209, 208, 33, 207, 206, 66, 205, 204, 1, 10, 40, 41, 64, 3, 16, 7, 90, 9, 6, 65, 5, 8, 32]
	south_st_ids = [24, 96, 21, 4, 15, 20, 11, 22, 13, 12, 14, 18, 19]

	num_radars_north = 0
	num_radars_south = 0
	num_cnts_poss_n = [0]*24
	num_cnts_poss_s = [0]*24
	gs_count_n = np.zeros(24)
	is_count_n = np.zeros(24)
	gs_count_s = np.zeros(24)
	is_count_s = np.zeros(24)

	filepath = '/data/fitcon/' + yr + '/' + mth + '/'
	file_string = sorted(np.array(os.listdir(filepath)))
	filtered = fnmatch.filter(file_string, str(date) + '.*')
	fitfiles = [filepath + x for x in filtered]
	good_files = np.where(np.array(fitfiles) != '/data/fitcon/2007/01/20070117.C0.han.fitacf.gz')
	fitfiles = np.array(fitfiles)[good_files]

	for file in fitfiles:
		# print 'The file is:', file
		start = time.time()

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
			# print 'Opening file ' + str(file) + ' took ' + str(end-start) + ' seconds'
		except EOFError as err:
			with open('errors_list', 'a') as f:
				f.write('{}\t{}\n'.format(file, err))
			print 'logged EOFError'
			continue
		except DmapDataError as err:
			with open('errors_list', 'a') as f:
				f.write('{}\t{}\n'.format(file, err))
			print 'logged corrupt file error'
			continue
		except EmptyFileError as err:
			with open('errors_list', 'a') as f:
				f.write('{}\t{}\n'.format(file, err))
			print 'logged data stream error'
			continue
		except:
			with open('errors_list', 'a') as f:
				f.write('{}\t{}\n'.format(file, 'unknown error'))
			print 'logged some other error'
			continue

		num_gates = 16
		# select data for range gates 0-15
		
		if records[0]['stid'] in north_st_ids:
			num_radars_north += 1
			list_hrs_n = []

			for i in range(len(records)):
				hr = records[i]['time.hr']
				list_hrs_n.append(hr)

				try:
					index = np.where(records[i]['slist'] < 16)[0]
					ranges = [records[i]['slist'][x] for x in index]
					gflg = [records[i]['gflg'][x] for x in index]

					gs_count_n[hr] += np.count_nonzero(gflg)
					pwr = [records[i]['pwr0'][x] for x in ranges]

					inx = np.where(gflg == 0)[0]
					is_count_n[hr] += np.count_nonzero([pwr[x] > 3. for x in inx])
				except:
					pass
			# Create the list of # records per hour for this radar times the number of gates, this is 
			# possible counts for this radar per hour
			counter_n = collections.Counter(list_hrs_n)
			num_poss_rdr_n = [x*num_gates for x in counter_n.values()]

			try:
				num_cnts_poss_n = [num_cnts_poss_n[x] + num_poss_rdr_n[x] for x in range(24)]
			except:
				missing_hrs = [x for x in range(24) if x not in counter_n.keys()]
				[num_poss_rdr_n.insert(x,0) for x in missing_hrs]
				num_cnts_poss_n = [num_cnts_poss_n[x] + num_poss_rdr_n[x] for x in range(24)]

		else:
			num_radars_south += 1
			list_hrs_s = []

			for i in range(len(records)):
				hr = records[i]['time.hr']
				list_hrs_s.append(hr)

				try:
					index = np.where(records[i]['slist'] < 16)[0]
					ranges = [records[i]['slist'][x] for x in index]
					gflg = [records[i]['gflg'][x] for x in index]

					gs_count_s[hr] += np.count_nonzero(gflg)
					pwr = [records[i]['pwr0'][x] for x in ranges]

					inx = np.where(gflg == 0)[0]
					is_count_s[hr] += np.count_nonzero([pwr[x] > 3. for x in inx])
				except:
					pass

			counter_s = collections.Counter(list_hrs_s)
			num_poss_rdr_s = [x*num_gates for x in counter_s.values()]

			try:
				num_cnts_poss_s = [num_cnts_poss_s[x] + num_poss_rdr_s[x] for x in range(24)]
			except:
				missing_hrs = [x for x in range(24) if x not in counter_s.keys()]
				[num_poss_rdr_s.insert(x,0) for x in missing_hrs]
				num_cnts_poss_s = [num_cnts_poss_s[x] + num_poss_rdr_s[x] for x in range(24)]

	with open('nh_first15_' + str(date), 'a') as north, open('sh_first15_' + str(date), 'a') as south:
		for hr in range(24):
			gs_frac_n = gs_count_n[hr]/num_cnts_poss_n[hr]
			is_frac_n = is_count_n[hr]/num_cnts_poss_n[hr]
			gs_frac_s = gs_count_s[hr]/num_cnts_poss_s[hr]
			is_frac_s = is_count_s[hr]/num_cnts_poss_s[hr]
			
			north.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(yr, mth, day, hr, gs_count_n[hr], is_count_n[hr], num_cnts_poss_n[hr], gs_frac_n, is_frac_n, num_radars_north))
			south.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(yr, mth, day, hr, gs_count_s[hr], is_count_s[hr], num_cnts_poss_s[hr], gs_frac_s, is_frac_s, num_radars_south))

if __name__ == '__main__':
	date = sys.argv[1]
	calc_counts_daily(date)