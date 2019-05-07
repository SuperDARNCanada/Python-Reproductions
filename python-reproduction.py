import backscatter.dmap.dmap as dm
import numpy as np
import os, sys
import gzip

north_st_ids = [209, 208, 33, 207, 206, 66, 205, 204, 1, 10, 40, 41, 64, 3, 16, 7, 90, 9, 6, 65, 5, 8, 32]
south_st_ids = [24, 96, 21, 4, 15, 20, 11, 22, 13, 12, 14, 18, 19]

for yr in range(1993,2019):
	for mth in range(1,13):
		for day in range(1,32):
			gs_count_n = np.zeros(24)
			is_count_n = np.zeros(24)
			gs_count_s = np.zeros(24)
			is_count_s = np.zeros(24)


			filepath = "/data/fitcon/" + str(yr) + "/" + str(mth).zfill(2) + "/"
			file_string = np.array(os.listdir(filepath))
# Eliminate known bad files
			good_files = file_string[np.where(file_string != '2001030500rC.fit.gz')]
			file_count = len(good_files)
#Add the filepath to each file string in good_files
			fitfiles = [filepath + x for x in good_files]

			if file_count > 0:
				num_radars_north = 0
				num_radars_south = 0
#Loop through fitfiles and open them, if they are zipped, unzip them
				for file in fitfiles:
					if ".gz" in file:
						with gzip.open(file, 'r') as f:
							raw_data = f.read()
						file_records = dm.parse_dmap_format_from_stream(raw_data)
					else:
						file_records = dm.parse_dmap_format_from_file(file)
#Loop through the records in the currently opened file
					for i in range(len(file_records)):
						if records[i]['stid'] in north_st_ids:
							num_radars_north = num_radars_north + 1
							hr = records[i]['time.hr']

							#Find ground scatter count in NH
							gs_count_n[hr] = gs_count_n[hr] + np.count_nonzero(records[i]['gflg'])

							#Find power values corresponding to ranges with data saved
							ranges = records[i]['slist']
							pwr = [records[i]['pwr0'][x] for x in ranges]

							#Find iono scatter count in NH
							inx = np.where(records[i]['gflg'] == 0)[0]
							is_count_n[hr] = is_count_n[hr] + np.count_nonzero([pwr[x] > 10. for x in inx])
						else:
							num_radars_south = num_radars_south + 1
							hr = records[i]['time.hr']

							#Find ground scatter count in SH
							gs_count_s[hr] = gs_count_s[hr] + np.count_nonzero(records[i]['gflg'])

							#Find power values corresponding to ranges with data saved
							ranges = records[i]['slist']
							pwr = [records[i]['pwr0'][x] for x in ranges]

							#Find iono scatter count in SH
							inx = np.where(records[i]['gflg'] == 0)[0]
							is_count_s[hr] = is_count_s[hr] + np.count_nonzero([pwr[x] > 10. for x in inx])

			for hr in range(0,24):
				with open('nh_data', 'r+') as north:
					north.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(yr, mth, day, hr, gs_count_n[hr], is_count_n[hr], num_radars_north))
				with open('sh_data', 'r+') as south:
					south.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(yr, mth, day, hr, gs_count_s[hr], is_count_s[hr], num_radars_south))
