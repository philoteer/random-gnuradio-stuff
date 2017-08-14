#!/usr/bin/env python2

import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

#./read.py filename -p val / -m filename.mat
if len(sys.argv) <= 1:
	print "usage"
	print "read.py 'filename' -p 0 : plot 0th block."
	print "read.py 'filename' -m matlab_filename : convert to matlab file."
	quit()
else:
	path = sys.argv[1]

if len(sys.argv) >= 4:
	mode = sys.argv[2]
	val = sys.argv[3]
else:
	mode = '-p'
	val = 0

#get data, time
data = np.fromfile(path,dtype=np.float32)
timestamp = np.fromfile(path,dtype=np.float64)

#reshape, drop first 2 cols (which is actually timestamp)
data = data.reshape(len(data)/58,58)
data = np.delete(data,0,1)
data = np.delete(data,0,1)

#drop data, and keep timestamp.
timestamp = timestamp.reshape(len(timestamp)/29,29)
timestamp = timestamp[:,0]

if mode == '-p':
	val = int(val)
	print timestamp[val]
	plt.plot(data[val])
	plt.show()

if mode == '-m':
	sio.savemat(val,{'data':data,'timestamp':timestamp})
