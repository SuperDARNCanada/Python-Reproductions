import backscatter.dmap.dmap as dm
import numpy as np
import os, sys

north = open('nh_data', 'r+')
south = open('sh_data', 'r+')

for yr in range(1993,2019)
	for mth in range(1,13)
		for day in range(1,32)
			filepath = "/data/fitcon/" + str(yr) + "/" + str(mth).zfill(2) + "/"; 
			file_string = np.array(os.listdir(filepath));
# Eliminate known bad files
			good_files = file_string[np.where(file_string != '2001030500rC.fit.gz')];
			file_count = len(good_files);
#Add the filepath to each file string in good_files
			fitfiles = [filepath + x for x in good_files];

			if file_count > 0
				num_radars_north = 0;
				num_radars_south = 0;
#Loop
				for idx, file in enumerate(fitfiles)
					file_records[idx] = dm.parse_dmap_format_from_file(file);



			


