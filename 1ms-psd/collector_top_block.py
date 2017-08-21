#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Nist
# Generated: Mon Aug 14 01:56:49 2017
##################################################

if __name__ == '__main__':
	import ctypes
	import sys
	if sys.platform.startswith('linux'):
		try:
			x11 = ctypes.cdll.LoadLibrary('libX11.so')
			x11.XInitThreads()
		except:
			print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
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
from fftprocess import fftprocess
from dumptofile import dumptofile
from consts import my_consts
import sip
import sys
import time


class nist(gr.top_block, Qt.QWidget):

	def __init__(self):
		gr.top_block.__init__(self, "Nist")
		Qt.QWidget.__init__(self)
		self.setWindowTitle("Nist")
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
		self.fft_len = fft_len = my_consts.fft_size()
		self.cal_dB = cal_dB = my_consts.cal_dB()
		self.window_compenstation = window_compenstation = 2
		self.target_freq = target_freq = my_consts.center_freq()
		self.samp_rate = samp_rate = my_consts.samp_rate()
		self.psd_normalization = psd_normalization = [1.0/fft_len]*fft_len
		self.lo_offset = lo_offset = my_consts.lo_offset()
		self.gain = gain = my_consts.LNA_gain()
		self.cal = cal = 10**((cal_dB-gain)/20)
		self.new_bin_size = new_bin_size = my_consts.agg_out()

		##################################################
		# Blocks
		##################################################
		self.uhd_usrp_source_0 = uhd.usrp_source(
			",".join(("", "")),
			uhd.stream_args(
				cpu_format="fc32",
				channels=range(1),
			),
		)
		self.uhd_usrp_source_0.set_samp_rate(samp_rate)
		self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(target_freq,lo_offset), 0)
		self.uhd_usrp_source_0.set_gain(gain, 0)
		self.uhd_usrp_source_0.set_antenna(my_consts.antenna_port(), 0)
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
		self.mul_const = blocks.multiply_const_vcc((psd_normalization))
		self.fft_vxx_0 = fft.fft_vcc(fft_len, True, (window.hann(fft_len)), True, 1)
		self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_len)
		self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, new_bin_size, 0)
		self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((cal * window_compenstation, ))
		self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fft_len)

		#my block
		self.fftprocess = fftprocess()
		self.dumptofile = dumptofile()
		##################################################
		# Connections
		##################################################
		# usrp -> calibration
		self.connect((self.uhd_usrp_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))

		#calibration -> vector
		self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_stream_to_vector_0, 0))

		#fft
		self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
		
		#fft -> PSD (normalization: by 1/N)
		self.connect((self.fft_vxx_0, 0), (self.mul_const, 0))
		self.connect((self.mul_const, 0), (self.blocks_complex_to_mag_squared_0, 0))
		
		#re-bin fft, max-hold (10 times).
		self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.fftprocess, 0))

		#to log
		self.connect((self.fftprocess, 0), (self.blocks_nlog10_ff_0, 0))
		
		#display (temporary)
		#self.connect((self.blocks_nlog10_ff_0, 0), (self.qtgui_vector_sink_f_0, 0))
		
		#data -> file
		self.connect((self.blocks_nlog10_ff_0, 0), (self.dumptofile, 0))

	def closeEvent(self, event):
		self.settings = Qt.QSettings("GNU Radio", "nist")
		self.settings.setValue("geometry", self.saveGeometry())
		event.accept()


	def get_fft_len(self):
		return self.fft_len

	def set_fft_len(self, fft_len):
		self.fft_len = fft_len
		self.set_psd_normalization([1.0/self.fft_len]*self.fft_len)

	def get_cal_dB(self):
		return self.cal_dB

	def set_cal_dB(self, cal_dB):
		self.cal_dB = cal_dB
		self.set_cal(10**((self.cal_dB-self.gain)/20))

	def get_window_compenstation(self):
		return self.window_compenstation

	def set_window_compenstation(self, window_compenstation):
		self.window_compenstation = window_compenstation
		self.blocks_multiply_const_vxx_0.set_k((self.cal * self.window_compenstation, ))

	def get_target_freq(self):
		return self.target_freq

	def set_target_freq(self, target_freq):
		self.target_freq = target_freq
		self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.target_freq,self.lo_offset), 0)

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

	def get_lo_offset(self):
		return self.lo_offset

	def set_lo_offset(self, lo_offset):
		self.lo_offset = lo_offset
		self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.target_freq,self.lo_offset), 0)

	def get_gain(self):
		return self.gain

	def set_gain(self, gain):
		self.gain = gain
		self.uhd_usrp_source_0.set_gain(self.gain, 0)
			

	def get_cal(self):
		return self.cal

	def set_cal(self, cal):
		self.cal = cal
		self.blocks_multiply_const_vxx_0.set_k((self.cal * self.window_compenstation, ))


def main(top_block_cls=nist, options=None):

	from distutils.version import StrictVersion
	if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
		style = gr.prefs().get_string('qtgui', 'style', 'raster')
		Qt.QApplication.setGraphicsSystem(style)
	qapp = Qt.QApplication(sys.argv)

	tb = top_block_cls()
	tb.start()
	tb.show()

	def quitting():
		tb.stop()
		tb.wait()
	qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
	qapp.exec_()


if __name__ == '__main__':
	main()
