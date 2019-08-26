# (C) SuperDARN Canada University of Saskatchewan 

# This code contains the necessary modification to run Python Multiprocessing
# and calculate the number of echos in each month of each year

import backscatter.dmap.dmap as dm
import numpy as np
import os, sys
import gzip
import bz2
from calendar import monthrange
import collections
import multiprocessing as mp
import time

north_st_ids = [209, 208, 33, 207, 206, 66, 205, 204, 1, 10, 40, 41, 64, 3, 16, 7, 90, 9, 6, 65, 5, 8, 32]
south_st_ids = [24, 96, 21, 4, 15, 20, 11, 22, 13, 12, 14, 18, 19]

for yr in range(2007,2008):
	for mth in range(1,2):
		manager = mp.Manager()
		# def convert_array_to_numpy(dim1, dim2, shared_array):
		# 	np_array = np.frombuffer(shared_array.get_obj())
		# 	np_array.reshape((dim1, dim2))

		#Create shared arrays and values
		num_days = monthrange(yr,mth)[1]
		# num_days = 6
		num_radars_north = mp.Array('i', num_days)
		num_radars_south = mp.Array('i', num_days)
		shared_gs_count_n = mp.Array('d', num_days*24)
		shared_is_count_n = mp.Array('d', num_days*24)
		shared_gs_count_s = mp.Array('d', num_days*24)
		shared_is_count_s = mp.Array('d', num_days*24)
		
		num_cnts_poss_n = manager.list([[0]*24]*num_days)
		num_cnts_poss_s = manager.list([[0]*24]*num_days)
		
		lock = mp.Lock()
		
		filepath = "/data/fitcon/" + str(yr) + "/" + str(mth).zfill(2) + "/"
		file_string = sorted(np.array(os.listdir(filepath)))
		file_count = len(file_string)

		#Add the filepath to each file string 
		fitfiles = [filepath + x for x in file_string]
		good_files = np.where(np.array(fitfiles) != '/data/fitcon/2007/01/20070117.C0.han.fitacf.gz')
		fitfiles = np.array(fitfiles)[good_files]

		def read_calculate(num_cnts_poss_n, num_cnts_poss_s, num_radars_north, num_radars_south, shared_gs_count_n, shared_is_count_n, shared_gs_count_s, shared_is_count_s, file, lock):
			start = time.time()
			if ".gz" in file:
				with gzip.open(file, 'r') as f:
					raw_data = f.read()
				records = dm.parse_dmap_format_from_stream(raw_data)
			elif ".bz2" in file:
				with bz2.BZ2File(file, 'r') as f:
					raw_data = f.read()
				records = dm.parse_dmap_format_from_stream(raw_data)
			else:
				records = dm.parse_dmap_format_from_file(file)
			end = time.time()
			print 'Opening file ' + str(file) + ' took ' + str(end-start) + 'seconds'

			day = records[0]['time.dy']

			if records[0]['stid'] in north_st_ids:
				print "Worker in the North!"
				lock.acquire()
				num_radars_north[day-1] += 1
				lock.release()

				list_hrs_n = []
				#Loop through the records in the currently opened file
				for i in range(len(records)):
					hr = records[i]['time.hr']
					list_hrs_n.append(hr)

					lock.acquire()
					try:
						idx = (day-1)*24 + hr
						#Find ground scatter count in NH
						shared_gs_count_n[idx] += np.count_nonzero(records[i]['gflg'])

						#Find power values corresponding to ranges with data saved
						ranges = records[i]['slist']
						pwr = [records[i]['pwr0'][x] for x in ranges]

						#Find iono scatter count in NH
						inx = np.where(records[i]['gflg'] == 0)[0]
						shared_is_count_n[idx] += np.count_nonzero([pwr[x] > 3. for x in inx])
					except:
						shared_gs_count_n[idx] += 0
						shared_is_count_n[idx] += 0
					lock.release()

				#Create the list of # records per hour for this radar x 75, this is possible counts for this radar per hour
				counter_n=collections.Counter(list_hrs_n)
				num_poss_rdr_n = [x*75 for x in counter_n.values()]

				#Add this list of possbile counts to list of total counts for all radars, per day
				lock.acquire()
				try:
					mod = num_cnts_poss_n[day-1]
					mod = [mod[x] + num_poss_rdr_n[x] for x in range(24)]
					num_cnts_poss_n[day-1] = mod
				except:
					missing_hrs = [x for x in range(24) if x not in counter_n.keys()]
					[num_poss_rdr_n.insert(x,0) for x in missing_hrs]
					mod = num_cnts_poss_n[day-1]
					mod = [mod[x] + num_poss_rdr_n[x] for x in range(24)]
					num_cnts_poss_n[day-1] = mod
				lock.release()

			else:
				print "Worker in the South!"
				lock.acquire()
				num_radars_south[day-1] += 1
				lock.release()

				list_hrs_s = []
				#Loop through the records in the currently opened file
				for i in range(len(records)):
					hr = records[i]['time.hr']
					list_hrs_s.append(hr)

					lock.acquire()
					try:
						idx = (day-1)*24 + hr
						#Find ground scatter count in SH
						shared_gs_count_s[idx] += np.count_nonzero(records[i]['gflg'])

						#Find power values corresponding to ranges with data saved
						ranges = records[i]['slist']
						pwr = [records[i]['pwr0'][x] for x in ranges]

						#Find iono scatter count in SH
						inx = np.where(records[i]['gflg'] == 0)[0]
						shared_is_count_s[idx] += np.count_nonzero([pwr[x] > 3. for x in inx])
					except:
						shared_gs_count_s[idx] += 0
						shared_is_count_s[idx] += 0
					lock.release()
					
				#Create the lists of # records per hour for this radar x 75, this is possible counts for this radar per hour
				counter_s = collections.Counter(list_hrs_s)
				num_poss_rdr_s = [x*75 for x in counter_s.values()]
				
				lock.acquire()
				try:
					#Add this list of possible counts to list of total counts for all radars, per day
					mod2 = num_cnts_poss_s[day-1]
					mod2 = [mod2[x] + num_poss_rdr_s[x] for x in range(24)]
					num_cnts_poss_s[day-1] = mod2
				except:
					missing_hrs = [x for x in range(24) if x not in counter_s.keys()]
					[num_poss_rdr_s.insert(x,0) for x in missing_hrs]
					mod2 = num_cnts_poss_s[day-1]
					mod2 = [mod2[x] + num_poss_rdr_s[x] for x in range(24)]
					num_cnts_poss_s[day-1] = mod2

				lock.release()

		def multiprocessing_helper(cnts_n, cnts_s, north, south, gs_n, is_n, gs_s, is_s, array, lock):
			for file in array:
				read_calculate(cnts_n, cnts_s, north, south, gs_n, is_n, gs_s, is_s, file, lock)

		if file_count > 0:
			fitfiles_split = np.array_split(fitfiles, 20)

			#Call function read_&_calculate for each file via multiprocessing
			processes = []
			for file_arr in fitfiles_split:
				p = mp.Process(target=multiprocessing_helper, args=(num_cnts_poss_n, num_cnts_poss_s, num_radars_north, num_radars_south, shared_gs_count_n, shared_is_count_n,
				 shared_gs_count_s, shared_is_count_s, file_arr, lock))
				processes.append(p)
				p.start()
			print len(processes)
			for p in processes:
				p.join()

		print "Almost done month: " + str(mth)

		gs_count_n = np.frombuffer(shared_gs_count_n.get_obj()).reshape((num_days,24))
		is_count_n = np.frombuffer(shared_is_count_n.get_obj()).reshape((num_days,24))
		gs_count_s = np.frombuffer(shared_gs_count_s.get_obj()).reshape((num_days,24))
		is_count_s = np.frombuffer(shared_is_count_s.get_obj()).reshape((num_days,24))

		start2 = time.time()
		with open('hourly_counts_' + str(yr) +'_nh', 'a') as north, open('hourly_counts_' + str(yr) + '_sh','a') as south:
			#Loop through days and hours and print to file
			for day in range(num_days):
				for hr in range(24):
					try:
						gs_frac_n = round(gs_count_n[day][hr]/num_cnts_poss_n[day][hr]*100, 4)
					except:
						gs_frac_n = float('nan')
					try:
						is_frac_n = round(is_count_n[day][hr]/num_cnts_poss_n[day][hr]*100, 4)
					except:
						is_frac_n = float('nan')
					try:
						gs_frac_s = round(gs_count_s[day][hr]/num_cnts_poss_s[day][hr]*100, 4)
					except:
						gs_frac_s = float('nan')
					try:
						is_frac_s = round(is_count_s[day][hr]/num_cnts_poss_s[day][hr]*100, 4)
					except:
						is_frac_s = float('nan')

					north.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(yr, mth, day+1, hr, gs_frac_n, is_frac_n, num_radars_north[day]))
					south.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(yr, mth, day+1, hr, gs_frac_s, is_frac_s, num_radars_south[day]))

		end2 = time.time()
		print 'writing takes' + str(end2-start2) + 'seconds'