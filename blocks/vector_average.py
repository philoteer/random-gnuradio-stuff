#!/usr/bin/env python

'''
Moving average of a input vector (float)
'''
import numpy
import Queue
from gnuradio import gr

#take average of a vector.
#in: a float32 vector (len = vec_len)
#out: a float32 vector (len = vec_len)

class vector_avg(gr.sync_block):

	#constructor
	def __init__(self, vec_len = 180, avg_len = 50, flush_rate = 4000, transients = 100):
		gr.sync_block.__init__(self,
			name="Moving Average",
			in_sig=[(numpy.float32,vec_len)],
			out_sig=[(numpy.float32,vec_len)])
			
		#Store arguments.
		
		#average length
		self.avg_len = avg_len
		
		#vector length
		self.vec_len = vec_len
		
		#average counter
		self.cnt = 0
		self.cnt_flusher = 0
		
		#result buffer
		self.result = numpy.zeros(vec_len)
		
		#auxilary result buffer (used for flushing the main buffer)
		self.result_secondary = numpy.zeros(vec_len)
		
		#flushes the main result buffer per flush_rate (to deal with possible ieee802.11 errors).
		self.flush_rate = flush_rate
		
		#A queue to store incoming data.
		self.data_queue = Queue.Queue(maxsize = self.avg_len)
		
		#Number of initial vector samples to drop.
		self.transients = transients
		
		
		#self.to_decibel = to_decibel

	#The main worker
	def work(self, input_items, output_items):

		
		in0 = input_items[0]
		out = output_items[0]
		
		#length of data to process
		proc_len = len(output_items[0])
		self.cnt += proc_len
		
		if self.cnt < self.transients:
				return proc_len
		
		#sum vectors that are to be processed (divided by the avg len later).
		for i in range (0, proc_len):
			self.result = self.result + in0[i]

			if self.cnt_flusher + self.avg_len > self.flush_rate:
				self.result_secondary = self.result_secondary + in0[i]

			if (self.data_queue.full()):
				self.result = self.result - self.data_queue.get()
				output_items[0][i] = self.result * (1.0/self.avg_len)
				
			self.data_queue.put(in0[i])
			self.cnt_flusher += 1

			if self.cnt_flusher > self.flush_rate:
				self.cnt_flusher = 0
				self.result = self.result_secondary
				self.result_secondary = numpy.zeros(self.vec_len)		
		
		#consume
		#self.consume(0, proc_len)
		return proc_len
