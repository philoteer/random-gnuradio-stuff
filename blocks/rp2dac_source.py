"""
Original code from Filip Dominec 2022, public domain
rp2daq, https://github.com/FilipDominec/rp2daq
(with GNU Radio embedded python template codes)
requires rp2daq be installed as a module, like i've done in https://github.com/philoteer/rp2daq_setup

TODO Fix:
Issue 1: finite "blocks_to_send" (will eventually stop transmitting)
Issue 2: Pi Pico may need to be resetted after each use (it will hang until the end of the "blocks_to_send" is reached).
"""

import sys
import rp2daq 
import time
import queue
import numpy as np
import threading
from gnuradio import gr

class blk(gr.sync_block):

	def __init__(self, samp_rate = 32): 
		gr.sync_block.__init__(
			self,
			name='rp2daq_adc',   # will show up in GRC 
			in_sig=[],
			out_sig=[np.float32,np.float32,np.float32]
		) 
		
		chs = [0,1,2]
		self.chs = chs
		self.rp = None
		self.all_data = []		
		self.main_queue = queue.Queue()
		self.block_size = 2000
		
		try:
			self.rp = rp2daq.Rp2daq()
			self.rp.pwm_configure_pair(pin=0, wrap_value=6553, clkdiv=25, clkdiv_int_frac=0)
			self.rp.pwm_set_value(pin=0, value=3000) 

			def append_ADC_data(**kwargs): 
				self.main_queue.put(kwargs['data'].copy())

			self.rp.internal_adc(channel_mask=sum(2**ch for ch in chs), 
					blocksize=self.block_size* len(chs), 
					blocks_to_send = 65535,
					clkdiv=48000//(samp_rate*len(chs)), 
					_callback=append_ADC_data)
		except: 
			print("error: no rp2daq device found.")
				
				
	def work(self, input_items, output_items):
		if(not(self.main_queue.empty()) and len(output_items[0]) >= self.block_size):
			out = (self.main_queue.get())
			output_items[0][0:self.block_size] = out[0::len(self.chs)]
			output_items[0][0:self.block_size] = (output_items[0][0:self.block_size] / 4096) - 0.5

			output_items[1][0:self.block_size] = out[1::len(self.chs)]
			output_items[1][0:self.block_size] = (output_items[1][0:self.block_size] / 4096) - 0.5

			output_items[2][0:self.block_size] = out[2::len(self.chs)]
			output_items[2][0:self.block_size] = (output_items[2][0:self.block_size] / 4096) - 0.5

			return self.block_size
		return 0
