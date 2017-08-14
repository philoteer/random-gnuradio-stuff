#!/usr/bin/env python

import numpy
from gnuradio import gr
import time

class fftprocess(gr.sync_block):

    def __init__(self):
		gr.sync_block.__init__(self,
			name="fftprocess",
			in_sig=[(numpy.float32,1250)],
			out_sig=[(numpy.float32,56)])
			
		self.hold_times = 10
		self.hold_cnt = 0
		self.start_time = time.time()

    def work(self, input_items, output_items):
		in0 = input_items[0]
		out = output_items[0]
		#number of fft blocks to generate during this iteration.
		cnt = min(len(in0)/self.hold_times, len(out))
		in_pos = 0
		
		#for each fft block to output
		for out_pos in range (0, cnt):
			#create one array
			out_current = numpy.zeros((56,), dtype=numpy.float32)

			#10 averages per each fft block
			for maxhold_pos in range (0, self.hold_times):
				#a = numpy.zeros((56,), dtype=numpy.float32)
				#aggregate (1008 pts -> 56 pts).
				#for x in range (120, 1129):
				#	a_pos = (x-121)/18
				#	a[a_pos] += in0[in_pos][x]
				a = in0[in_pos][121:1129].reshape((56, 18))
				a = numpy.sum(a, axis=1)
				
				#max hold.
				for x in range (0, 56):
					out_current[x] = max(out_current[x], a[x])

				#move to next input data.
				in_pos += 1

			#add the new fft block to the output buffer.
			out[out_pos] = out_current
		#consume, return.
		self.consume_each(cnt * self.hold_times)
		return cnt
