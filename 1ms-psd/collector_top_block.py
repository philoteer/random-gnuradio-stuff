#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Nist
# Generated: Mon Aug 14 01:56:49 2017
##################################################

##################################################
#The Top flow graph; upon execution, it automatically collects PSD estimates of the configured
#Channel (configured in const.py) and stores the results to a file (again, configured in
#const.py) . 
##################################################

#if ran as a main program:
if __name__ == '__main__':
	import ctypes
	import sys
	if sys.platform.startswith('linux'):
		try:
			x11 = ctypes.cdll.LoadLibrary('libX11.so')
			x11.XInitThreads()
		except:
			print "Warning: failed to XInitThreads()"

#import
from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
from dumptofile import dumptofile
from consts import my_consts
import sip
import sys
import time
import osmosdr

#Dynamically select the fftprocess block for optimal results.
if my_consts.hold_times() > 50:
	from fftprocess_large import fftprocess
else:
	from fftprocess import fftprocess

#top block class start
class nist(gr.top_block, Qt.QWidget):

	#init
	def __init__(self):
		#init the top block and GUI.
		gr.top_block.__init__(self, "Nist-v2")
		Qt.QWidget.__init__(self)
		self.setWindowTitle("Nist-v2")
		try:
			self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
		except:
			pass
		self.top_scroll_layout = Qt.QVBoxLayout()
		self.setLayout(self.top_scroll_layout)
		self.top_scroll = Qt.QScrollArea()
		self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
		self.top_scroll_layout.addWidget(self.top_scroll)
		self.top_scroll.setWidgetResizable(True)
		self.top_widget = Qt.QWidget()
		self.top_scroll.setWidget(self.top_widget)
		self.top_layout = Qt.QVBoxLayout(self.top_widget)
		self.top_grid_layout = Qt.QGridLayout()
		self.top_layout.addLayout(self.top_grid_layout)

		self.settings = Qt.QSettings("GNU Radio", "nist")
		self.restoreGeometry(self.settings.value("geometry").toByteArray())

		##################################################
		# Variables
		##################################################
		
		#FFT Len, Calibration factor, Windowing function compensation.
		self.fft_len = fft_len = my_consts.fft_size()
		self.cal_dB = cal_dB = my_consts.cal_dB()
		self.window_compenstation = window_compenstation = 2.0
		
		#Target freq / sampling rate
		self.target_freq = target_freq = my_consts.center_freq()
		self.samp_rate = samp_rate = my_consts.samp_rate()
		
		#PSD adjustment factor (calculated using above variables)
		self.psd_normalization = psd_normalization = ([(window_compenstation/fft_len) **2 ]*my_consts.agg_out()) #(2.0/FFT_SIZE) ^2 (applied after fft -> mag^2 to save processing power)

		#calibration (applies the calibration factor and undo the power increase due to the amplifier gain).
		self.cal = cal = 10**((cal_dB-my_consts.usrp_gain())/20)
		if (my_consts.source_type() == "OSMOCOM"):
			self.cal = cal = 10**((cal_dB-my_consts.osmosdr_RF_gain() - my_consts.osmosdr_IF_gain() - my_consts.osmosdr_BB_gain())/20)
		self.new_bin_size = new_bin_size = my_consts.agg_out()

		#for usrp
		self.usrp_lo_offset = usrp_lo_offset = my_consts.usrp_lo_offset()
		self.usrp_gain = usrp_gain = my_consts.usrp_gain()

		#for osmosdr
		self.osmosdr_RF_gain = osmosdr_RF_gain = my_consts.osmosdr_RF_gain()
		self.osmosdr_IF_gain = osmosdr_IF_gain = my_consts.osmosdr_IF_gain()
		self.osmosdr_BB_gain = osmosdr_BB_gain = my_consts.osmosdr_BB_gain()

		##################################################
		# Blocks
		##################################################
		
		#------------------------------signal source------------------------------
		#dummy signal mode		
		if my_consts.source_type() == "CONST":
			self.uhd_usrp_source_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 1)
		
		#usrp mode
		elif my_consts.source_type() == "USRP":
			self.uhd_usrp_source_0 = uhd.usrp_source(
				",".join(("", "")),
				uhd.stream_args(
					cpu_format="fc32",
					channels=range(1),
				),
			)
			self.uhd_usrp_source_0.set_samp_rate(samp_rate)
			self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(target_freq,usrp_lo_offset), 0)
			self.uhd_usrp_source_0.set_gain(usrp_gain, 0)
			self.uhd_usrp_source_0.set_antenna(my_consts.antenna_port(), 0)

		#osmosdr mode
		elif my_consts.source_type() == "OSMOCOM":
			self.uhd_usrp_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
			self.uhd_usrp_source_0.set_sample_rate(samp_rate)
			self.uhd_usrp_source_0.set_center_freq(target_freq, 0)
			self.uhd_usrp_source_0.set_freq_corr(0, 0)
			self.uhd_usrp_source_0.set_dc_offset_mode(0, 0)
			self.uhd_usrp_source_0.set_iq_balance_mode(0, 0)
			self.uhd_usrp_source_0.set_gain_mode(False, 0)
			self.uhd_usrp_source_0.set_gain(osmosdr_RF_gain, 0)
			self.uhd_usrp_source_0.set_if_gain(osmosdr_IF_gain, 0)
			self.uhd_usrp_source_0.set_bb_gain(osmosdr_BB_gain, 0)
			self.uhd_usrp_source_0.set_antenna(my_consts.antenna_port(), 0)
			self.uhd_usrp_source_0.set_bandwidth(samp_rate, 0)
		#------------------------------signal source end--------------------------

		#junks (removed QT gui)
		self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
			new_bin_size,
			0,
			1.0,
			"x-Axis",
			"y-Axis",
			"",
			1 # Number of inputs
		)
		#self.qtgui_vector_sink_f_0.set_update_time(0.10)
		#self.qtgui_vector_sink_f_0.set_y_axis(-140, 10)
		#self.qtgui_vector_sink_f_0.enable_autoscale(False)
		#self.qtgui_vector_sink_f_0.enable_grid(False)
		#self.qtgui_vector_sink_f_0.set_x_axis_units("")
		#self.qtgui_vector_sink_f_0.set_y_axis_units("")
		#self.qtgui_vector_sink_f_0.set_ref_level(0)
		
		#labels = ["", "", "", "", "",
		#		  "", "", "", "", ""]
		#widths = [1, 1, 1, 1, 1,
		#		  1, 1, 1, 1, 1]
		#colors = ["blue", "red", "green", "black", "cyan",
		#		  "magenta", "yellow", "dark red", "dark green", "dark blue"]
		#alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
		#		  1.0, 1.0, 1.0, 1.0, 1.0]
		#for i in xrange(1):
		#	if len(labels[i]) == 0:
		#		self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
		#	else:
		#		self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
		#	self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
		#	self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
		#	self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])
		
		#self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.pyqwidget(), Qt.QWidget)
		#self.top_layout.addWidget(self._qtgui_vector_sink_f_0_win)

		#PSD Normalizer / FFT / log10 / data -> Mag^2 blocks
		self.mul_const = blocks.multiply_const_vff((psd_normalization))
		self.fft_vxx_0 = fft.fft_vcc(fft_len, True, (window.hann(fft_len)), True, my_consts.fft_threads())
		self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_len)
		self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, new_bin_size, 0)
		self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fft_len)

		#if calibration needed: create cal block
		if abs(cal) > 0.1:
			self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((cal, ))

		#my blocks (process/aggregrate FFT data / dump data to files)
		self.fftprocess = fftprocess()
		self.dumptofile = dumptofile()

		#debug blocks (performance eval, etc)
		if my_consts.debug_mode():
			self.blocks_probe_rate_0 = blocks.probe_rate(gr.sizeof_float*self.fft_len, 1000.0, 0.15)
			self.blocks_message_debug_0 = blocks.message_debug()

		#throws out n-1 snapshots and use only 1 for calculation
		self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*fft_len, my_consts.keep_1_fft_blk_per_n())

		##################################################
		# Connections
		##################################################
		if abs(cal) > 0.1:	#if calibration needed:
			# usrp -> calibration
			self.connect((self.uhd_usrp_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))

			#calibration -> vector
			self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_stream_to_vector_0, 0))

		else:	#if calibration not needed:
			# usrp -> vector
			self.connect((self.uhd_usrp_source_0, 0), (self.blocks_stream_to_vector_0, 0))

		#Throw out n-1 snapshots and keep 1
		self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_keep_one_in_n_0, 0))

		#fft -> mag^2
		self.connect((self.blocks_keep_one_in_n_0, 0), (self.fft_vxx_0, 0))
		self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
		
		#re-bin fft, max-hold.
		self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.fftprocess, 0))

		#normalize by multiplying ((window compensation)/N)^2
		self.connect((self.fftprocess, 0), (self.mul_const, 0))

		#to log
		self.connect((self.mul_const, 0), (self.blocks_nlog10_ff_0, 0))
		
		#display (temporary)
		#self.connect((self.blocks_nlog10_ff_0, 0), (self.qtgui_vector_sink_f_0, 0))
		
		#data -> file
		self.connect((self.blocks_nlog10_ff_0, 0), (self.dumptofile, 0))

		#debug blocks
		
		#performance eval
		if my_consts.debug_mode():
			self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_probe_rate_0, 0))
			self.msg_connect((self.blocks_probe_rate_0, 'rate'), (self.blocks_message_debug_0, 'print'))

	#exit event
	def closeEvent(self, event):
		self.settings = Qt.QSettings("GNU Radio", "nist")
		self.settings.setValue("geometry", self.saveGeometry())
		event.accept()

	#------Accessors, Mutators------------------
	def get_fft_len(self):
		return self.fft_len

	def set_fft_len(self, fft_len):
		self.fft_len = fft_len
		self.set_psd_normalization([(window_compenstation/fft_len) **2 ]*my_consts.agg_out())

	def get_cal_dB(self):
		return self.cal_dB

	def set_cal_dB(self, cal_dB):
		self.cal_dB = cal_dB
		self.set_cal(10**((self.cal_dB-self.usrp_gain)/20))

	def get_window_compenstation(self):
		return self.window_compenstation

	def set_window_compenstation(self, window_compenstation):
		self.window_compenstation = window_compenstation
		self.set_psd_normalization([(window_compenstation/fft_len) **2 ]*my_consts.agg_out())


	def get_target_freq(self):
		return self.target_freq

	def set_target_freq(self, target_freq):
		self.target_freq = target_freq
		self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.target_freq,self.usrp_lo_offset), 0)

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

	def get_psd_normalization(self):
		return self.psd_normalization

	def set_psd_normalization(self, psd_normalization):
		self.psd_normalization = psd_normalization
		self.mul_const.set_k((self.psd_normalization))

	def get_usrp_lo_offset(self):
		return self.usrp_lo_offset

	def set_usrp_lo_offset(self, usrp_lo_offset):
		self.usrp_lo_offset = usrp_lo_offset
		self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.target_freq,self.usrp_lo_offset), 0)

	def get_usrp_gain(self):
		return self.usrp_gain

	def set_usrp_gain(self, usrp_gain):
		self.usrp_gain = usrp_gain
		self.uhd_usrp_source_0.set_gain(self.usrp_gain, 0)
			
	def get_cal(self):
		return self.cal

	def set_cal(self, cal):
		self.cal = cal
		self.blocks_multiply_const_vxx_0.set_k((self.cal, ))
	#------Accessors, Mutators end------------------

#The main function 
def main(top_block_cls=nist, options=None):

	#Qt init
	from distutils.version import StrictVersion
	if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
		style = gr.prefs().get_string('qtgui', 'style', 'raster')
		Qt.QApplication.setGraphicsSystem(style)
	qapp = Qt.QApplication(sys.argv)

	#Top block init / start
	tb = top_block_cls()
	tb.start()
	tb.show()

	def quitting():
		tb.stop()
		tb.wait()
	qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
	qapp.exec_()

#If ran as a main program, run the 'main' fct above.
if __name__ == '__main__':
	main()
