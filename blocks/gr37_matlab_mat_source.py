import numpy as np
from gnuradio import gr
import scipy.io as sio


class blk(gr.sync_block):  
	
	def __init__(self, file_path="/some/path/raw_tx.mat", var_name = "x_cg"):  # only default arguments here
		"""arguments to this function show up as parameters in GRC"""
		gr.sync_block.__init__(
			self,
			name='Matlab/Octave mat Source',   # will show up in GRC
			in_sig=[],
			out_sig=[np.complex64]
		)

		self.file_path = file_path
		self.var_name = var_name
		
		self.loaded_data = sio.loadmat(self.file_path)
		self.out_data = np.squeeze(self.loaded_data[self.var_name])
		self.data_len = len(self.out_data)
		self.pointer = 0

	def work(self, input_items, output_items):
		
		out_len = min(len(output_items[0]), self.data_len - self.pointer)

		output_items[0][0:out_len] = self.out_data[self.pointer:self.pointer + out_len]

		self.pointer = self.pointer + out_len
		self.pointer = self.pointer % self.data_len

		return out_len
		
