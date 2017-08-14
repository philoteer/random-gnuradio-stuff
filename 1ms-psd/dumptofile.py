#!/usr/bin/env python

import numpy
from gnuradio import gr
import time
import datetime

def generatefilename():
	a = datetime.datetime.utcnow().isoformat()+".754sp"
	a = a.replace(":","_")	#Windows file name quirk
	print "New file: " + a
	return a

class dumptofile(gr.sync_block):		

	def __init__(self):
		gr.sync_block.__init__(self,
			name="dumptofile",
			in_sig=[(numpy.float32,56)],
			out_sig=None)
			
		self.aggregate_length = 1000 * 1800 # 30 min
		self.cnt = 0
		self.opened_file = open(generatefilename(),'wb')

	def work(self, input_items, output_items):
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
			self.opened_file = open(generatefilename(),'wb')
		
		#consume, return.
		self.consume_each(len(in0))
		return 0
