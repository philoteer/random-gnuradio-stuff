#!/usr/bin/env python

import numpy
from gnuradio import gr
import time
from consts import my_consts

class fftprocess(gr.basic_block):

	def __init__(self):
		gr.basic_block.__init__(self,
			name="fftprocess",
			in_sig=[(numpy.float32,my_consts.fft_size())],
			out_sig=[(numpy.float32,my_consts.agg_out())],
			)

		#consts
		self.hold_times = my_consts.hold_times()
		self.fft_size = my_consts.fft_size()
		self.agg_out = my_consts.agg_out()
		self.start_time = time.time()

		#mutable vars
		self.hold_cnt = 0	#counts fft blocks processed so far (resets once reaches hold_times)
		self.out_current = numpy.zeros((self.agg_out * my_consts.in_bins_per_out_bin(),), dtype=numpy.float32)	#current block
		

	def general_work(self, input_items, output_items):
		in0 = input_items[0]
		out = output_items[0]

		#get number of pts to process
		num_process = min(self.hold_times - self.hold_cnt, len(in0))
		
		#max hold		
		if num_process >= 1:
			a = numpy.max(in0[:,my_consts.psd_start():my_consts.psd_end()],0)
			self.out_current = numpy.maximum(self.out_current,a)		
						
		#consume
		self.consume_each(num_process)
		self.hold_cnt += num_process

		#if we need to output: do so.
		if(self.hold_cnt == self.hold_times) and (len(out) >= 1):
			self.hold_cnt = 0
			if(my_consts.in_bins_per_out_bin() != 1):
				a = self.out_current.reshape((self.agg_out, my_consts.in_bins_per_out_bin()))
				a = numpy.sum(a, axis=1)
			else:
				a = self.out_current
			out[0] = a
			self.out_current = numpy.zeros((self.agg_out  * my_consts.in_bins_per_out_bin(),), dtype=numpy.float32)
			return 1

		#if not: skip.
		else:
			return 0
		
