#!/usr/bin/env python2

import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import scipy.interpolate
from consts import my_consts

#./read.py filename -p val / -m filename.mat
if len(sys.argv) <= 1:
	print "usage"
	print "read.py 'filename' -p 0 : plot 0th block."
	print "read.py 'filename' -m matlab_filename : convert to matlab file."
	print "read.py 'filename' -w 100 500 : plot waterfall, from 100 th blk to 500 th blk."
	quit()
else:
	path = sys.argv[1]

if len(sys.argv) == 4:
	mode = sys.argv[2]
	val = sys.argv[3]

if len(sys.argv) == 5:
	mode = sys.argv[2]
	val_1 = sys.argv[3]
	val_2 = sys.argv[4]

#get data, time
data = np.fromfile(path,dtype=np.float32)
timestamp = np.fromfile(path,dtype=np.float64)

#reshape, drop first 2 cols (which is actually timestamp)
data = data.reshape(len(data)/(my_consts.agg_out()+2),(my_consts.agg_out()+2))
data = np.delete(data,0,1)
data = np.delete(data,0,1)

#drop data, and keep timestamp.
timestamp = timestamp.reshape(len(timestamp)/((my_consts.agg_out()+2)/2),((my_consts.agg_out()+2)/2))
timestamp = timestamp[:,0]

if mode == '-p':
	val = int(val)
	print timestamp[val]
	plt.plot(data[val])
	plt.show()

if mode == '-m':
	sio.savemat(val,{'data':data,'timestamp':timestamp})

#The part below is copy-paste job from https://stackoverflow.com/questions/33282368/plotting-a-2d-heatmap-with-matplotlib
if mode == '-w':
	plt.imshow(data[int(val_1):int(val_2),:], cmap='hot', interpolation='nearest')
	plt.show()
