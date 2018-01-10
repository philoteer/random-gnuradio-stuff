#!/usr/bin/env python

#A simple GNU Radio block, which dumps received vectors into files.
#Needs consts.py to function
import numpy
from gnuradio import gr
import time
import datetime
import subprocess
from consts import my_consts

#Generate a new file name (uses timestamp).
def generatefilename():		
	a = datetime.datetime.utcnow().isoformat()+".754sp"
	a = a.replace(":","_")	#Windows file name quirk
	print "New file: " + a
	return a

#The main block class
class dumptofile(gr.basic_block):		

	#Constructor.
	#input signal: float32 vector with length my_consts.agg_out() (defined in consts.py).
	#output signal: none (sink type).
	def __init__(self):
		gr.basic_block.__init__(self,
			name="dumptofile",
			in_sig=[(numpy.float32,my_consts.agg_out())],
			out_sig=None)
			
		#set consts, vars
		self.aggregate_length = int((my_consts.samp_rate()/my_consts.fft_size())/(my_consts.hold_times()*my_consts.keep_1_fft_blk_per_n()) * my_consts.time_length_per_file())
		#print str(self.aggregate_length)
		self.cnt = 0
		self.opened_file_name = generatefilename()
		self.opened_file = open(self.opened_file_name,'wb')

	#the main worker
	def general_work(self, input_items, output_items):
		#init_time = time.time()
		in0 = input_items[0]		
		
		#get time
		current_time = numpy.float64(time.time())
		
		#Process all data at once
		self.cnt += len(in0)		
		
		#for every input data:
		for x in range (0, len(in0)):
			#write to file
			self.opened_file.write(numpy.float64(current_time))
			self.opened_file.write(in0[x])
		
		#create a new file if counter is filled
		if (self.cnt >= self.aggregate_length):
			self.cnt = 0
			self.opened_file.close()
			
			#if upload option is on, upload the file to a remote server.
			if (my_consts.upload_file()):
				subprocess.Popen(["curl", "-F", "pw="+my_consts.upload_pw(),"-F","fileformID=@"+self.opened_file_name,my_consts.upload_path()])
				
			self.opened_file_name = generatefilename()
			self.opened_file = open(self.opened_file_name,'wb')
		
		#consume, return.
		self.consume_each(len(in0))
		#end_time = time.time()
		#print "dump2file - time: " + str(end_time - init_time)
		return 0
