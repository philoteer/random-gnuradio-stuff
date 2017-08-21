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
			
		self.hold_times = my_consts.hold_times()
		self.hold_cnt = 0
		self.start_time = time.time()
		self.temp = 0
		
		self.fft_size = my_consts.fft_size()
		self.agg_out = my_consts.agg_out()

    def general_work(self, input_items, output_items):
		in0 = input_items[0]
		out = output_items[0]
		#number of fft blocks to generate during this iteration.
		cnt = min(len(in0)/self.hold_times, len(out))
		in_pos = 0
		
		#for each fft block to output
		for out_pos in range (0, cnt):
			#create one array
			out_current = numpy.zeros((self.agg_out,), dtype=numpy.float32)

			#10 averages per each fft block
			for maxhold_pos in range (0, self.hold_times):
				#a = numpy.zeros((56,), dtype=numpy.float32)
				#aggregate (1008 pts -> 56 pts).
				a = in0[in_pos][my_consts.psd_start():my_consts.psd_end()].reshape((self.agg_out, my_consts.in_bins_per_out_bin()))
				a = numpy.sum(a, axis=1)
				
				#max hold.
				#for x in range (0, self.agg_out):
				#	out_current[x] = max(out_current[x], a[x])
				out_current = numpy.maximum(out_current,a)
				
				#move to next input data.
				in_pos += 1

			#add the new fft block to the output buffer.
			out[out_pos] = out_current
		#consume, return.
		self.consume_each(cnt * self.hold_times)

		return cnt
