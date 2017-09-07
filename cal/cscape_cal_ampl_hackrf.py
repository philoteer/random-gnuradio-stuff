#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Amplitude calibration tool for USRP/UBX
# Author: Dave Aragon
# Written:	 Mon Sep  5 2016
# Last Edited: Fri Sep  9 2016
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

import osmosdr
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import numbersink2
from gnuradio.wxgui import pubsub
from gnuradio.wxgui import number_window
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import datetime
import wx


class usrp_cal_amp(grc_wxgui.top_block_gui):

	def __init__(self, samp_rate=2e6):

		grc_wxgui.top_block_gui.__init__(self, title="Amplitude calibration tool for USRP, v 0.2")

		########################################################
		# TODO: See if there's a sensible way to package an icon
		#	   with this program, rather than rely on some 
		#	   particular Gnu Radio user's installation.
		#
		# _icon_path = "/home/dave/.local/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		# self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))
		########################################################

		##################################################
		# Parameters
		#
		# TODO: Add enough parameters, and the right ones,
		#	   that the program will come up with sliders
		#	set conveniently for the user.
		#	When step-sweep support is implemented, we
		#	want to be able to run even w/o the GUI.
		##################################################
		self.samp_rate = samp_rate

		##################################################
		# Variables
		##################################################
		self.usrp_gain_slider = usrp_gain_slider = 20
		self.usrp_freq_offset_slider = usrp_freq_offset_slider = -100000
		self.input_signal_power = input_signal_power = -50
		self.input_freq_slider = input_freq_slider = 1e9
		self.cal_file = None

		##################################################
		# Blocks
		##################################################

		self._input_rowhdr_text_box = wx.StaticText(
			self.GetWin(), 
			label='\nReference Signal:\n'
		)
		font = self._input_rowhdr_text_box.GetFont()
		font.SetWeight(wx.FONTWEIGHT_BOLD)
		self._input_rowhdr_text_box.SetFont(font)
		self.GridAdd(self._input_rowhdr_text_box, 1, 1, 1, 1)

		_input_freq_slider_sizer = wx.BoxSizer(wx.VERTICAL)
		self._input_freq_slider_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_input_freq_slider_sizer,
			value=self.input_freq_slider,
			callback=self.set_input_freq_slider,
			label='RF input frequency (Hz)',
			converter=forms.float_converter(),
			proportion=0,
		)
		self._input_freq_slider_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_input_freq_slider_sizer,
			value=self.input_freq_slider,
			callback=self.set_input_freq_slider,
			minimum=10e6,
			maximum=6000e6,
			num_steps=20,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_input_freq_slider_sizer, 1, 2, 1, 3)

		_input_signal_power_sizer = wx.BoxSizer(wx.VERTICAL)
		self._input_signal_power_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_input_signal_power_sizer,
			value=self.input_signal_power,
			callback=self.set_input_signal_power,
			label='Input signal power (dBm)',
			converter=forms.float_converter(),
			proportion=0,
		)
		self._input_signal_power_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_input_signal_power_sizer,
			value=self.input_signal_power,
			callback=self.set_input_signal_power,
			minimum=-70,
			maximum=-20,
			num_steps=50,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_input_signal_power_sizer, 1, 5, 1, 2)

		self._row_spacer_1 = wx.StaticText(
			self.GetWin(), 
			label="\n"
		)
		self.GridAdd(self._row_spacer_1, 2, 1, 1, 6)

		self._sdr_rowhdr_text_box = wx.StaticText(
			self.GetWin(), 
			label='HackRF:'
		)
		font = self._sdr_rowhdr_text_box.GetFont()
		font.SetWeight(wx.FONTWEIGHT_BOLD)
		self._sdr_rowhdr_text_box.SetFont(font)
		self.GridAdd(self._sdr_rowhdr_text_box, 3, 1, 1, 1)

		_usrp_freq_offset_slider_sizer = wx.BoxSizer(wx.VERTICAL)
		self._usrp_freq_offset_slider_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_usrp_freq_offset_slider_sizer,
			value=self.usrp_freq_offset_slider,
			callback=self.set_usrp_freq_offset_slider,
			label='Freq offset',
			converter=forms.float_converter(),
			proportion=0,
		)
		self._usrp_freq_offset_slider_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_usrp_freq_offset_slider_sizer,
			value=self.usrp_freq_offset_slider,
			callback=self.set_usrp_freq_offset_slider,
			minimum=-200000,
			maximum=200000,
			num_steps=5,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_usrp_freq_offset_slider_sizer, 3, 2, 1, 3)

		_usrp_gain_slider_sizer = wx.BoxSizer(wx.VERTICAL)
		self._usrp_gain_slider_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_usrp_gain_slider_sizer,
			value=self.usrp_gain_slider,
			callback=self.set_usrp_gain_slider,
			label='Gain (dB) !!!8dB step!!!',
			converter=forms.float_converter(),
			proportion=0,
		)
		self._usrp_gain_slider_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_usrp_gain_slider_sizer,
			value=self.usrp_gain_slider,
			callback=self.set_usrp_gain_slider,
			minimum=0,
			maximum=38,
			num_steps=38,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)


		self.GridAdd(_usrp_gain_slider_sizer, 3, 5, 1, 2)

		self._row_spacer_2 = wx.StaticText(
			self.GetWin(), 
			label=""
		)
		self.GridAdd(self._row_spacer_2, 4, 1, 1, 6)

		self.wxgui_numbersink2_0_0 = numbersink2.number_sink_f(
			self.GetWin(),
			unit='dBFS',
			minval=-100,
			maxval=10,
			factor=1.0,
			decimal_places=0,
			ref_level=0,
			sample_rate=samp_rate/10,
			number_rate=10,
			average=False,
			avg_alpha=None,
			label='Output power (digital)',
			peak_hold=False,
			show_gauge=True,
		)
		self.GridAdd(self.wxgui_numbersink2_0_0.win, 5, 1, 1, 2)


		self.wxgui_numbersink2_0_0_1 = numbersink2.number_sink_f(
			self.GetWin(),
			unit='dB',
			minval=-20,
			maxval=80,
			factor=1.0,
			decimal_places=0,
			ref_level=0,
			sample_rate=samp_rate/10,
			number_rate=10,
			average=False,
			avg_alpha=None,
			label='Power conversion value\n(output dbFS -> input dBm + gain)',
			peak_hold=False,
			show_gauge=True,
		)
		self.GridAdd(self.wxgui_numbersink2_0_0_1.win, 5, 4, 1, 3)

		self.data_capture_button = forms.single_button(
			parent=self.GetWin(),
			label="Capture this data point",
			callback=self.checkbox_event,
			style=wx.BU_EXACTFIT,
		)
		font = self.data_capture_button._button.GetFont()
		font.SetWeight(wx.FONTWEIGHT_BOLD)
		self.data_capture_button._button.SetFont(font)
		self.GridAdd(self.data_capture_button, 6, 4, 1, 1)

		self._wrapup_text_box_1 = wx.StaticText(
			self.GetWin(), 
			label='\n   USRP LO freq:\n',
		)
		font = self._wrapup_text_box_1.GetFont()
		font.SetWeight(wx.FONTWEIGHT_BOLD)
		self._wrapup_text_box_1.SetFont(font)
		self.GridAdd(self._wrapup_text_box_1, 6, 5, 1, 1)

		self._wrapup_text_box_1.SetLabel("\n   USRP LO freq: {0:.0f}\n".format(
			self.input_freq_slider + self.usrp_freq_offset_slider))
	
		self._wrapup_text_box_2 = wx.StaticText(
			self.GetWin(), 
			label='\n\n',
		)
		self.GridAdd(self._wrapup_text_box_2, 6, 6, 1, 1)


		self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
		self.osmosdr_source_0.set_sample_rate(samp_rate)
		self.osmosdr_source_0.set_center_freq(input_freq_slider + usrp_freq_offset_slider, 0)
		self.osmosdr_source_0.set_freq_corr(0, 0)
		self.osmosdr_source_0.set_dc_offset_mode(0, 0)
		self.osmosdr_source_0.set_iq_balance_mode(0, 0)
		self.osmosdr_source_0.set_gain_mode(False, 0)
		self.osmosdr_source_0.set_gain(0, 0)
		self.osmosdr_source_0.set_if_gain(usrp_gain_slider, 0)
		self.osmosdr_source_0.set_bb_gain(0, 0)
		self.osmosdr_source_0.set_antenna('', 0)
		self.osmosdr_source_0.set_bandwidth(samp_rate, 0)

		self.u = self.osmosdr_source_0

		self.u_mboard_serial = ""
		self.u_dboard_serial = ""
		self.u_dboard_id = ""
		self.u_dboard_id = ""

		self._sdr_rowhdr_text_box.SetLabel("USRP serial # {0:s}  \n{1:s} serial # {2:s}  ".format(
			self.u_mboard_serial,
			self.u_dboard_id,
			self.u_dboard_serial))

		self.single_pole_iir_filter_xx_1_0 = filter.single_pole_iir_filter_ff(1.0/((0.1)* samp_rate), 1)
		self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
			1, samp_rate, samp_rate/5, samp_rate/10, firdes.WIN_HAMMING, 6.76))
		self.dc_blocker_xx_0 = filter.dc_blocker_cc(1000, True)
		self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_gr_complex*1, '', ""); self.blocks_tag_debug_0.set_display(True)
		self.blocks_sub_xx_0 = blocks.sub_ff(1)
		self.blocks_nlog10_ff_0_0 = blocks.nlog10_ff(10, 1, 0)
		self.blocks_keep_one_in_n_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, 10)
		self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_float*1, 10)
		self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(1)
		self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, input_signal_power+usrp_gain_slider)

		##################################################
		# Connections
		##################################################
		self.connect((self.analog_const_source_x_0, 0), (self.blocks_keep_one_in_n_0_0, 0))	
		self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.single_pole_iir_filter_xx_1_0, 0))	
		self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_sub_xx_0, 1))	
		self.connect((self.blocks_keep_one_in_n_0, 0), (self.wxgui_numbersink2_0_0, 0))	
		self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_sub_xx_0, 0))	
		self.connect((self.blocks_nlog10_ff_0_0, 0), (self.blocks_keep_one_in_n_0, 0))	
		self.connect((self.blocks_sub_xx_0, 0), (self.wxgui_numbersink2_0_0_1, 0))	
		self.connect((self.dc_blocker_xx_0, 0), (self.low_pass_filter_0, 0))	
		self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))	
		self.connect((self.single_pole_iir_filter_xx_1_0, 0), (self.blocks_nlog10_ff_0_0, 0))	
		self.connect((self.u, 0), (self.blocks_tag_debug_0, 0))	
		self.connect((self.u, 0), (self.dc_blocker_xx_0, 0))	

	def checkbox_event(self, evt):
		lineout = "{0:.0f}, {1:+2.0f}\n".format(
			self.input_freq_slider + self.usrp_freq_offset_slider,
			self.wxgui_numbersink2_0_0_1.win['value_real'])
		print(lineout)
		self.cal_file.append(lineout)

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.u.set_sample_rate(self.samp_rate)
		self.single_pole_iir_filter_xx_1_0.set_taps(1.0/((0.1)* self.samp_rate))
		self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.samp_rate/5, self.samp_rate/10, firdes.WIN_HAMMING, 6.76))

	def get_usrp_gain_slider(self):
		return self.usrp_gain_slider

	def set_usrp_gain_slider(self, usrp_gain_slider):
		self.usrp_gain_slider = usrp_gain_slider
		self._usrp_gain_slider_slider.set_value(self.usrp_gain_slider)
		self._usrp_gain_slider_text_box.set_value(self.usrp_gain_slider)
		self.osmosdr_source_0.set_if_gain(self.usrp_gain_slider, 0)
			
		self.analog_const_source_x_0.set_offset(self.input_signal_power+self.usrp_gain_slider)

	def get_usrp_freq_offset_slider(self):
		return self.usrp_freq_offset_slider

	def set_usrp_freq_offset_slider(self, usrp_freq_offset_slider):
		self.usrp_freq_offset_slider = usrp_freq_offset_slider
		self._usrp_freq_offset_slider_slider.set_value(self.usrp_freq_offset_slider)
		self._usrp_freq_offset_slider_text_box.set_value(self.usrp_freq_offset_slider)
		self.osmosdr_source_0.set_center_freq(self.input_freq_slider + self.usrp_freq_offset_slider, 0)
		self._wrapup_text_box_1.SetLabel("\n   USRP LO freq: {0:.0f}\n".format(
			self.input_freq_slider + self.usrp_freq_offset_slider))

	def get_input_signal_power(self):
		return self.input_signal_power

	def set_input_signal_power(self, input_signal_power):
		self.input_signal_power = input_signal_power
		self._input_signal_power_slider.set_value(self.input_signal_power)
		self._input_signal_power_text_box.set_value(self.input_signal_power)
		self.analog_const_source_x_0.set_offset(self.input_signal_power+self.usrp_gain_slider)

	def get_input_freq_slider(self):
		return self.input_freq_slider

	def set_input_freq_slider(self, input_freq_slider):
		self.input_freq_slider = input_freq_slider
		self._input_freq_slider_slider.set_value(self.input_freq_slider)
		self._input_freq_slider_text_box.set_value(self.input_freq_slider)
		self.osmosdr_source_0.set_center_freq(self.input_freq_slider + self.usrp_freq_offset_slider, 0)
		self._wrapup_text_box_1.SetLabel("\n   USRP LO freq: {0:.0f}\n".format(
			self.input_freq_slider + self.usrp_freq_offset_slider))

	def set_cal_file(self, calfile):
		self.cal_file = calfile


class cal_file:

	def __init__(self, tb):

		self.creation_time = datetime.datetime.utcnow()
		self.fname = "rx_cal_ampl_{0:s}_{1:s}.csv".format(
				tb.u_mboard_serial, tb.u_dboard_serial)
				# self.creation_time.strftime("%Y%b%dT%H%M%S"))

		with open(self.fname, 'w') as fd:
			fd.write('version, 0.1, Cityscape SDR calibration table\n')
			fd.write('name, Rx gain vs. frequency\n')
			fd.write("SDR, N2xx, {0:s}\n".format(tb.u_mboard_serial))
			fd.write("RF front end, {0:s}, {1:s}\n".format(
				tb.u_dboard_id, tb.u_dboard_serial))


			fd.write("timestamp, {0:s}, {1:s} \n".format(
					self.creation_time.strftime("%s"),
					self.creation_time.strftime("%c")))
				
			fd.write("source, {0:s}\n".format( __file__ ))

			fd.write("DATA STARTS HERE\n")
			fd.write("frequency, gain_adj\n")


	def append(self, line):
		with open(self.fname, 'a') as fd:
			fd.write(line)

def argument_parser():
	parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
	parser.add_option(
		"-s", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(2e6),
		help="Set samplerate [default=%default]")
	return parser


def main(top_block_cls=usrp_cal_amp, options=None):
	if options is None:
		options, _ = argument_parser().parse_args()

	tb = top_block_cls(samp_rate=options.samp_rate)

	calfile = cal_file(tb)
	tb.set_cal_file(calfile)

	tb.Start(True)
	tb.Wait()


if __name__ == '__main__':
	main()
