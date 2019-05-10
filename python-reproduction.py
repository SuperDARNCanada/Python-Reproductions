import backscatter.dmap.dmap as dm
import numpy as np
import os, sys
import gzip
import bz2
from calendar import monthrange
import collections

north_st_ids = [209, 208, 33, 207, 206, 66, 205, 204, 1, 10, 40, 41, 64, 3, 16, 7, 90, 9, 6, 65, 5, 8, 32]
south_st_ids = [24, 96, 21, 4, 15, 20, 11, 22, 13, 12, 14, 18, 19]

for yr in range(2007,2008):
	for mth in range(1,13):
		num_days = monthrange(yr, mth)[1]
		gs_count_n = np.zeros((num_days,24))
		is_count_n = np.zeros((num_days,24))
		gs_count_s = np.zeros((num_days,24))
		is_count_s = np.zeros((num_days,24))
		num_cnts_poss_n = [[0]*24]*num_days
		num_cnts_poss_s = [[0]*24]*num_days


		filepath = "/data/fitcon/" + str(yr) + "/" + str(mth).zfill(2) + "/"
		file_string = sorted(np.array(os.listdir(filepath)))
		file_count = len(file_string)
		
		#Add the filepath to each file string, remove the bad file
		fitfiles = [filepath + x for x in file_string]
		good_files = np.where(np.array(fitfiles) != '/data/fitcon/2007/01/20070117.C0.han.fitacf.gz')
		fitfiles = np.array(fitfiles)[good_files]

		if file_count > 0:
			num_radars_north = 0
			num_radars_south = 0
			
			#Loop through fitfiles and open them, if they are zipped, unzip them
			for file in fitfiles:
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

				day = records[0]['time.dy']

				if records[0]['stid'] in north_st_ids:
					num_radars_north = num_radars_north + 1
					list_hrs_n = []
					#Loop through the records in the currently opened file
					for i in range(len(records)):
						hr = records[i]['time.hr']
						list_hrs_n.append(hr)

						#Check for a gflg array
						# if records[i].keys().count('gflg') == 0:
						try:
							#Find ground scatter count in NH
							gs_count_n[day-1][hr] = gs_count_n[day-1][hr] + np.count_nonzero(records[i]['gflg'])

							#Find power values corresponding to ranges with data saved
							ranges = records[i]['slist']
							pwr = [records[i]['pwr0'][x] for x in ranges]

							#Find iono scatter count in NH
							inx = np.where(records[i]['gflg'] == 0)[0]
							is_count_n[day-1][hr] = is_count_n[day-1][hr] + np.count_nonzero([pwr[x] > 3. for x in inx])
						except:
							gs_count_n[day-1][hr] = None
							is_count_n[day-1][hr] = None

					#Create the list of # records per hour for this radar x 75, this is possible counts for this radar per hour
					counter_n=collections.Counter(list_hrs_n)
					num_poss_rdr_n = [x*75 for x in counter_n.values()]
					#Add this list of possbile counts to list of total counts for all radars, per day
					try:
						num_cnts_poss_n[day-1] = [num_cnts_poss_n[day-1][x] + num_poss_rdr_n[x] for x in range(24)]
					except:
						missing_hrs = [x for x in range(24) if x not in counter_n.keys()]
						[num_poss_rdr_n.insert(x,0) for x in missing_hrs]
						num_cnts_poss_n[day-1] = [num_cnts_poss_n[day-1][x] + num_poss_rdr_n[x] for x in range(24)]


				else:
					num_radars_south = num_radars_south + 1
					list_hrs_s = []
					#Loop through the records in the currently opened file
					for i in range(len(records)):
						hr = records[i]['time.hr']
						list_hrs_s.append(hr)

						#Check for a gflg array
						#if records[i].keys().count('gflg') == 0:
						try:
							#Find ground scatter count in SH
							gs_count_s[day-1][hr] = gs_count_s[day-1][hr] + np.count_nonzero(records[i]['gflg'])

							#Find power values corresponding to ranges with data saved
							ranges = records[i]['slist']
							pwr = [records[i]['pwr0'][x] for x in ranges]

							#Find iono scatter count in SH
							inx = np.where(records[i]['gflg'] == 0)[0]
							is_count_s[day-1][hr] = is_count_s[day-1][hr] + np.count_nonzero([pwr[x] > 3. for x in inx])
						except:
							gs_count_s[day-1][hr] = None
							is_count_s[day-1][hr] = None

					#Create the lists of # records per hour for this radar x 75, this is possible counts for this radar per hour
					counter_s = collections.Counter(list_hrs_s)
					num_poss_rdr_s = [x*75 for x in counter_s.values()]
					print file
					
					try:
						#Add this list of possible counts to list of total counts for all radars, per day
						num_cnts_poss_s[day-1] = [num_cnts_poss_s[day-1][x] + num_poss_rdr_s[x] for x in range(24)]
					except:
						missing_hrs = [x for x in range(24) if x not in counter_s.keys()]
						[num_poss_rdr_s.insert(x,0) for x in missing_hrs]
						num_cnts_poss_s[day-1] = [num_cnts_poss_s[day-1][x] + num_poss_rdr_s[x] for x in range(24)]

		with open('nh_data', 'w') as north, open('sh_data','w') as south:
			#Loop through days and hours and print to file
			for day in range(num_days):
				for hr in range(24):
					gs_frac_n = gs_count_n[day][hr]/num_cnts_poss_n[day][hr]
					is_frac_n = is_count_n[day][hr]/num_cnts_poss_n[day][hr]
					gs_frac_s = gs_count_s[day][hr]/num_cnts_poss_s[day][hr]
					is_frac_s = is_count_s[day][hr]/num_cnts_poss_s[day][hr]
					
					north.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(yr, mth, day, hr, gs_frac_n, is_frac_n, num_radars_north))
					south.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(yr, mth, day, hr, gs_frac_s, is_frac_s, num_radars_south))
