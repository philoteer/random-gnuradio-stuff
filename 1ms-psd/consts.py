#!/usr/bin/env python

class my_consts:	
	#Data Collection Config
	@staticmethod
	def time_length_per_file():
		return 1800	#1800s = 30min per file
	@staticmethod
	def cal_dB():
		return  -9.0	#for dB -> dBm calibration
	@staticmethod
	def center_freq():
		return  709e6	#709MHz
	@staticmethod
	def samp_rate():
		return  12.5e6	#12.5MS/s
	@staticmethod
	def lo_offset():
		return  -12.5e6	#-12.5MHz
	@staticmethod
	def LNA_gain():
		return  20	#20dB
	@staticmethod
	def antenna_port():
		return  "RX2"	#TX/RX or RX2

	#FFT Config
	@staticmethod
	def fft_size():
		return 1250	#original FFT size
		
	#Aggregation Config
	@staticmethod
	def agg_out():
		return 56		#PSD length after aggregation
	@staticmethod
	def hold_times():
		return 10		#How much PSD samples to max hold
	@staticmethod
	def in_bins_per_out_bin():
		return 18		#18 PSD bins in -> 1 PSD bin out
	@staticmethod
	def psd_start():
		return 121		#first 121 points from the input FFT data are dropped.
	@staticmethod
	def psd_end():
		return 1129	#data after the 1129th point from the input FFT data are dropped.
		
