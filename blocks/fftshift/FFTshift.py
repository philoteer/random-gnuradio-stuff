#!/usr/bin/env python
from gnuradio import gr
from gnuradio import blocks
from gnuradio import digital
import time
import numpy

#applies fftshift to a vecter.
#Input: float32 (length: size)
#Output: float32 (length: size)

class FFTshift(gr.basic_block):
	#constructor
	def __init__(self,size,drop_when_overloaded):
		gr.basic_block.__init__(self, name="FFT_Shift",
			in_sig=[(numpy.float32,size)],
			out_sig=[(numpy.float32,size)])
		self.drop_true = drop_when_overloaded

	#run
	def general_work(self, input_items, output_items):
		in0 = input_items[0]
		out = output_items[0]

		#check input/output buffer len
		if len(out) >= len(in0):
			ps_len = len(in0)
			consume_len = ps_len
		elif self.drop_true:
			ps_len = len(out)
			consume_len = len(in0)
		else:
			ps_len = len(out)
			consume_len = ps_len
				
		#do
		for cnt in range(0,ps_len):
			out[cnt] = numpy.fft.fftshift(in0[cnt])
		
		#consume, return	
		self.consume_each(consume_len)
		return ps_len
