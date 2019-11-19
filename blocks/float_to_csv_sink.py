import numpy as np
from gnuradio import gr

class blk(gr.sync_block):  
	
	def __init__(self, file_path="/some/path/out.dat", delimiter = "\n"):  # only default arguments here
		"""arguments to this function show up as parameters in GRC"""
		gr.sync_block.__init__(
			self,
			name='Delimated Text Sink (Float)',   # will show up in GRC
			in_sig=[np.float32],
			out_sig=[]
		)

		self.file_path = file_path
		self.f = open(file_path, "w")
		self.delimiter = delimiter;

	def work(self, input_items, output_items):
		
		proc_len = len(input_items[0])

		x = np.char.mod('%f', input_items[0])
		x_str = self.delimiter.join(x)
		self.f.write(x_str);
		self.f.write(self.delimiter);
		return proc_len
		
