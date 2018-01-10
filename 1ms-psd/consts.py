#!/usr/bin/env python

#Stores various constants used by the flow graph.
class my_consts:	
	#Data Collection Config
	
	#time length per each file
	@staticmethod
	def time_length_per_file():
		return 3600	#3600 = 1H per file
	
	#dBFS -> dBm calibration factor (added to the measurement results)
	#For this, assume that the gain setting of the USRP (or the SDR) is 0dB.
	@staticmethod
	def cal_dB():
		return  0.0	#for dB -> dBm calibration
		
	#rcvr center freq
	@staticmethod
	def center_freq():
		return  3.625e9	#3.625GHz center freq
	
	#rcvr samp rate
	@staticmethod
	def samp_rate():
		return  200e6	#200MS/s

	#!UHD Source ONLY!
	#Local oscillator offset (for DC offset removal, etc)
	@staticmethod
	def usrp_lo_offset():	#-12.5MHz offset
		return  0	

	#!UHD Source ONLY!
	#UHD gain
	@staticmethod
	def usrp_gain():
		return  15	#15dB
	
	#!GR-OSMOSDR only!
	#OSMOCOM Source RF Gain
	@staticmethod
	def osmosdr_RF_gain():
		return 0

	#!GR-OSMOSDR only!
	#OSMOCOM Source IF Gain
	@staticmethod
	def osmosdr_IF_gain():
		return 0

	#!GR-OSMOSDR only!
	#OSMOCOM Source Baseband Gain
	@staticmethod
	def osmosdr_BB_gain():
		return 0

	#Antenna port
	@staticmethod
	def antenna_port():
		return  "RX2"	#TX/RX or RX2

	#FFT Config
	#FFT len (total - before re-binning)
	@staticmethod
	def fft_size():
		return 200	#original FFT size

	#Multithreaded? (recommended: leave this to one; it is unlikely to impact the performance positively).
	@staticmethod
	def fft_threads():
		return  1	## of fft threads		
	
	#FFT Re-binning / Aggregation Config
	#Output vector length
	@staticmethod
	def agg_out():
		return 150		#PSD length after aggregation
	
	#Number of times to average.
	@staticmethod
	def hold_times():
		return 50000		#How much PSD samples to max hold
		
	#Re-binnig ratio (n/b, where n is number of input FFT bins, b is output FFT bins)
	@staticmethod
	def in_bins_per_out_bin():
		return 1		#1 PSD bins in -> 1 PSD bin out

	#Number of points to throw out (beginning)
	@staticmethod
	def psd_start():
		return 25		#first 25 points from the input FFT data are dropped.

	#Number of points to throw out (end)
	@staticmethod
	def psd_end():
		return 175		#data after the 175th point from the input FFT data are dropped.

	#Radio type (A constant, synthethic source; UHD USRP; or OSMOCOM)	
	@staticmethod
	def source_type():
		return "CONST"		#CONST, USRP, or OSMOCOM

	#Turn on/off the debug mode.
	@staticmethod
	def debug_mode():
		return True	

	#FFT vector reduction (for faster calculation): out of n FFT vectors, only 1 is used for calculation.
	@staticmethod
	def keep_1_fft_blk_per_n():
		return 10		#Out of 10 fft_len snapshots, only 1 is used for the calculation.

	#Automatic remote file upload mode
	@staticmethod
	def upload_file():
		return True		#auto-upload (curl needed)

	#File upload path
	@staticmethod
	def upload_path():
		return "http://piloteer.wo.tc/~piloteer/test/upload.php"		#data after the 1129th point from the input FFT data are dropped.
		
	#File upload PW
	@staticmethod
	def upload_pw():
		return "PDP11"
