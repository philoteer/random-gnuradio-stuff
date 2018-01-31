#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr
import pmt

class psd_aggregator(gr.basic_block):
	"""
	docstring for block psd_aggregator
	"""
	def __init__(self, f_start,f_end,fft_len,total_len):
		gr.basic_block.__init__(self,
			name="psd_aggregator",
			in_sig=[(numpy.float32,fft_len)],
			out_sig=[(numpy.float32,total_len)])
			
		self.f_start = f_start
		self.f_end = f_end
		self.fft_len = fft_len
		self.total_len = total_len
		self.current_freq = -1
		
		self.start_psd = -200
		self.transient_pkts = 30
		self.last_freq_change = -1

		self.vec_out = numpy.zeros((total_len),dtype=float)
		self.vec_out = self.vec_out +self.start_psd
	'''
	def forecast(self, noutput_items, ninput_items_required):
		#setup size of input_items[i] for work call
		for i in range(len(ninput_items_required)):
			ninput_items_required[i] = noutput_items
	'''
	def general_work(self, input_items, output_items):
		in0 = input_items[0]
		out = output_items[0]		
		nread = self.nitems_read(0)

		#for each data vector:
		for x in range (0, len(in0)):
			#locate tag (if exist)
			tags = self.get_tags_in_range(0,nread+x,nread+x+1,pmt.string_to_symbol("rx_freq"))
			#if tag exist: update, skip.
			if len(tags) != 0:
				self.current_freq =  pmt.to_double(tags[0].value)
				self.last_freq_change = nread+x
				
			#if tag does not exist and the transient period has ended:
			elif self.current_freq != -1 and (nread+x - self.last_freq_change) > self.transient_pkts:
				#find relative frequency
				total_freq_diff = self.f_end - self.f_start
				current_freq_diff = self.current_freq - self.f_start
				
				relative_pos_of_centre_freq = current_freq_diff / total_freq_diff
				
				#if the relative freq lies between 0 and 1: 
				if (relative_pos_of_centre_freq) >= 0 and  (relative_pos_of_centre_freq) <= 1:
					#find the array index
					centre_index = relative_pos_of_centre_freq * self.total_len
					begin_index = int(max(0, centre_index - (self.fft_len/2)))
					end_index = int(min(self.total_len, centre_index + (self.fft_len/2)))
					
					#update the array.
					if (end_index - begin_index == self.fft_len):
						self.vec_out[begin_index:end_index] = in0[x]
				
		self.consume_each(len(input_items[0]))

		if len(out) == 0:
			return 0
		else:
			out[0] = self.vec_out
			return 1
