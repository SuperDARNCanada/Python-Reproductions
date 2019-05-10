import backscatter.dmap.dmap as dm
import numpy as np
import os, sys
import gzip
import bz2

for yr in range(2007,2008):
	for mth in range(1,13):
		filepath = "/data/fitcon/" + str(yr) + "/" + str(mth).zfill(2) + "/"
		file_string = sorted(np.array(os.listdir(filepath)))
		file_count = len(file_string)
		
		#Add the filepath to each file string 
		fitfiles = [filepath + x for x in file_string]
		if file_count > 0:
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

				find_nogflg=[records[x].keys().count('gflg') == 0 for x in range(len(records))]
				no_gflg=np.where(np.array(find_nogflg)==True)

				if len(no_gflg[0]) > 0:
					with open('files_without_glflg_arrays', 'w') as f:
						f.write('{}\n'.format(file))
