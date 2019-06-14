import numpy as np
import os, sys
from calendar import monthrange
import collections
from datetime import datetime as dt
import matplotlib.pyplot as plt

yr = np.loadtxt('nh_allgates_2007')[:,0]
mth = np.loadtxt('nh_allgates_2007')[:,1]
day = np.loadtxt('nh_allgates_2007')[:,2]
hr = np.loadtxt('nh_allgates_2007')[:,3]
gs_count = np.loadtxt('nh_allgates_2007')[:,4]
is_count = np.loadtxt('nh_allgates_2007')[:,5]
total_count = np.loadtxt('nh_allgates_2007')[:,6]
gs_frac = np.loadtxt('nh_allgates_2007')[:,7]
is_frac = np.loadtxt('nh_allgates_2007')[:,8]
num_rdrs = np.loadtxt('nh_allgates_2007')[:,9]
time_array = np.zeros(length(yr))

for i, (m, d, h) in enumerate(zip(mth, day, hr)):
	time_array[i] = dt(m,d,h)

plt.figure(1)
plt.plot(time_array, gs_count)
plt.show()