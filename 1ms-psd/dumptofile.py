#!/usr/bin/env python

import numpy
from gnuradio import gr
import time
import datetime
import subprocess
from consts import my_consts

def generatefilename():		
	a = datetime.datetime.utcnow().isoformat()+".754sp"
	a = a.replace(":","_")	#Windows file name quirk
	print "New file: " + a
	return a

class dumptofile(gr.basic_block):		

	def __init__(self):
		gr.basic_block.__init__(self,
			name="dumptofile",
			in_sig=[(numpy.float32,my_consts.agg_out())],
			out_sig=None)
			
		self.aggregate_length = int((my_consts.samp_rate()/my_consts.fft_size())/(my_consts.hold_times()*my_consts.keep_1_fft_blk_per_n()) * my_consts.time_length_per_file())
		#print str(self.aggregate_length)
		self.cnt = 0
		self.opened_file_name = generatefilename()
		self.opened_file = open(self.opened_file_name,'wb')

	def general_work(self, input_items, output_items):
		#init_time = time.time()
		in0 = input_items[0]		
		current_time = numpy.float64(time.time())
		self.cnt += len(in0)		
		
		for x in range (0, len(in0)):
			self.opened_file.write(numpy.float64(current_time))
			self.opened_file.write(in0[x])
		
		#create a new file if counter is filled
		if (self.cnt >= self.aggregate_length):
			self.cnt = 0
			self.opened_file.close()
			
			if (my_consts.upload_file()):
				subprocess.Popen(["curl", "-F", "pw="+my_consts.upload_pw(),"-F","fileformID=@"+self.opened_file_name,my_consts.upload_path()])
				
			self.opened_file_name = generatefilename()
			self.opened_file = open(self.opened_file_name,'wb')
		
		#consume, return.
		self.consume_each(len(in0))
		#end_time = time.time()
		#print "dump2file - time: " + str(end_time - init_time)
		return 0
