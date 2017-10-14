#!/usr/bin/env python

class my_consts:	
	#Data Collection Config
	@staticmethod
	def time_length_per_file():
		return 3600	#3600 = 1H per file
	@staticmethod
	def cal_dB():
		return  0.0	#for dB -> dBm calibration
	@staticmethod
	def center_freq():
		return  3.625e9	#3.625GHz center freq
	@staticmethod
	def samp_rate():
		return  200e6	#200MS/s
	#UHD Source ONLY
	@staticmethod
	def usrp_lo_offset():	#-12.5MHz offset
		return  0	
	#UHD Source ONLY
	@staticmethod
	def usrp_gain():
		return  15	#15dB
	
	#OSMOSDR only
	@staticmethod
	def osmosdr_RF_gain():
		return 0

	#OSMOSDR only
	@staticmethod
	def osmosdr_IF_gain():
		return 0

	#OSMOSDR only
	@staticmethod
	def osmosdr_BB_gain():
		return 0


	@staticmethod
	def antenna_port():
		return  "RX2"	#TX/RX or RX2

	#FFT Config
	@staticmethod
	def fft_size():
		return 200	#original FFT size
	@staticmethod
	def fft_threads():
		return  1	## of fft threads		
	#Aggregation Config
	@staticmethod
	def agg_out():
		return 150		#PSD length after aggregation
	@staticmethod
	def hold_times():
		return 50000		#How much PSD samples to max hold
	@staticmethod
	def in_bins_per_out_bin():
		return 1		#18 PSD bins in -> 1 PSD bin out
	@staticmethod
	def psd_start():
		return 25		#first 121 points from the input FFT data are dropped.
	@staticmethod
	def psd_end():
		return 175		#data after the 1129th point from the input FFT data are dropped.
		
	@staticmethod
	def source_type():
		return "CONST"		#CONST, USRP, or OSMOCOM

	@staticmethod
	def debug_mode():
		return True		#data after the 1129th point from the input FFT data are dropped.

	@staticmethod
	def keep_1_fft_blk_per_n():
		return 10		#Out of 4 fft_len snapshots, only 1 is used for the calculation.

	@staticmethod
	def upload_file():
		return True		#auto-upload (curl needed)

	@staticmethod
	def upload_path():
		return "http://piloteer.wo.tc/~piloteer/test/upload.php"		#data after the 1129th point from the input FFT data are dropped.
		
	@staticmethod
	def upload_pw():
		return "PDP11"
