#!/usr/bin/env python
from gnuradio import gr
from gnuradio import blocks
from gnuradio import digital
import numpy

#Input: a float32 vector, in length 'size'
#Output: a float32 vector, in length 'size_new'
#Arg: "start" indicates the start of the output vector.

class vector_slice(gr.basic_block):
	#constructor
	def __init__(self,size,size_new,start):
		gr.basic_block.__init__(self, name="vector_slice",
			in_sig=[(numpy.float32,size)],
			out_sig=[(numpy.float32,size_new)])

		self.size_new = size_new
		self.startval = start

	#"size_new" variable mutator
	def update_size(self,size_new):
		self.size_new = size_new

	#"start" variable mutator
	def update_start(self,start):
		self.startval = start

	#main function
	def general_work(self, input_items, output_items):
		in0 = input_items[0]
		out = output_items[0]

		#Check vector length (ensure that I do not cause the buffer overrun).
		if len(out) >= len(in0):
			ps_len = len(in0)
			consume_len = ps_len
		else:
			ps_len = len(out)
			consume_len = ps_len

		#Slice!		
		for cnt in range(0,ps_len):
			out[cnt] = in0[cnt][self.startval:(self.startval+self.size_new)]

		#Consume, return.		
		self.consume_each(consume_len)
		return ps_len
