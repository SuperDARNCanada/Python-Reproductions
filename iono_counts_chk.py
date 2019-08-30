# (C) SuperDARN Canada University of Saskatchewan 
# Test code for error in ionospheric counts calculation, error was found to be related
# to Python array notation and searching
import backscatter.dmap.dmap as dm
import numpy as np
import fnmatch
import os, sys
import gzip
import bz2
from calendar import monthrange
import collections

def find_arrays(date):
	yr = str(date)[:4]
	mth = str(date)[4:6]
	day = str(date)[6:8]
	north_st_ids = [209, 208, 33, 207, 206, 66, 205, 204, 1, 10, 40, 41, 64, 3, 16, 7, 90, 9, 6, 65, 5, 8, 32]
	south_st_ids = [24, 96, 21, 4, 15, 20, 11, 22, 13, 12, 14, 18, 19]

	filepath = '/data/fitcon/' + yr + '/' + mth + '/'
	file_string = sorted(np.array(os.listdir(filepath)))
	filtered = fnmatch.filter(file_string, str(date) + '.*')
	fitfiles = [filepath + x for x in filtered]
	good_files = np.where(np.array(fitfiles) != '/data/fitcon/2007/01/20070117.C0.han.fitacf.gz')
	fitfiles = np.array(fitfiles)[good_files]

	for file in fitfiles:
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
		# print 'Opening file ' + str(file) + ' took ' + str(end-start) + ' seconds'

		#Save the gflg and slist arrays to see why iono counts are zero
		for x in range(len(records)):
			try:
				idx = records[x]['slist']
				pwr = [records[x]['pwr0'][i] for i in idx]

				if records[0]['stid'] in north_st_ids:
					with open('check_ionoN_' + str(date), 'a') as f:
						f.write('{}\n'.format(file))
						f.write('{}\t{}\t{}\n'.format(idx, records[x]['gflg'], pwr))
				elif records[0]['stid'] in south_st_ids:
					with open('check_ionoS_' + str(date), 'a') as f:
						f.write('{}\n'.format(file))
						f.write('{}\t{}\t{}\n'.format(idx, records[x]['gflg'], pwr))
			except:
				if records[0]['stid'] in north_st_ids:
					with open('check_ionoN_' + str(date), 'a') as f:
						f.write('{}\t{}\n'.format(file, 'there was a problem'))
				elif records[0]['stid'] in south_st_ids:
					with open('check_ionoS_' + str(date), 'a') as f:
						f.write('{}\t{}\n'.format(file, 'there was a problem'))

if __name__ == '__main__':
	date = sys.argv[1]
	find_arrays(date)