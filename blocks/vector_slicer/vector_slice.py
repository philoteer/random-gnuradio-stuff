#!/usr/bin/env python
from gnuradio import gr
from gnuradio import blocks
from gnuradio import digital
import numpy

#cherrypick part of a vector
class vector_slice(gr.basic_block):
	#constructor
	def __init__(self,size,size_new,start):
		gr.basic_block.__init__(self, name="FFT_Shift",
			in_sig=[(numpy.float32,size)],
			out_sig=[(numpy.float32,size_new)])

		self.length = size_new
		self.start = start
		
	def update_length(self, length_new):
		self.length = length_new
	
	def update_start(self, start_new):
		self.start = start_new
	
	#run
	def general_work(self, input_items, output_items):
		in0 = input_items[0]
		out = output_items[0]
		
		ps_len = len(in0)
		consume_len = ps_len	
		
		for cnt in range(0,ps_len):
			out[cnt] = in0[cnt][self.start:self.length]
		
		self.consume_each(consume_len)
		return ps_len
