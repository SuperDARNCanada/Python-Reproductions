import backscatter.dmap.dmap as dm
import numpy as np
import os, sys
import gzip
import bz2
from calendar import monthrange
import collections
import multiprocessing as mp
import time

yr = 2007
mth = 4

filepath = "/data/fitcon/" + str(yr) + "/" + str(mth).zfill(2) + "/"
file_string = sorted(np.array(os.listdir(filepath)))
file_count = len(file_string)

#Add the filepath to each file string 
fitfiles = [filepath + x for x in file_string]
good_files = np.where(np.array(fitfiles) != '/data/fitcon/2007/01/20070117.C0.han.fitacf.gz')
fitfiles = np.array(fitfiles)[good_files]

with gzip.open(fitfiles[0], 'r') as f:
	raw_data = f.read()
records = dm.parse_dmap_format_from_stream(raw_data)

thirt_ctr = 0
start = time.time()
for rec in records:
	if rec['bmnum'] == 13:
		 thirt_ctr += 1
end = time.time()
print(thirt_ctr)
print(end - start)
