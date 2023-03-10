import numpy as np
from gnuradio import gr

import time
import socket

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

	def __init__(self, server_ip = "192.168.0.1", server_port = 80):  # only default arguments here
		gr.sync_block.__init__(
			self,
			name='Custom UDP Sink',   # will show up in GRC
			in_sig=[np.float32],
			out_sig=[]
		)
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.dest = (server_ip, server_port)
		self.pkt_max_len = 508

	def work(self, input_items, output_items):
		cnt = 0
		data_tx = input_items[0].tobytes()
		data_len = len(data_tx)
		
		while ((cnt * self.pkt_max_len) < data_len): 
			self.sock.sendto(data_tx[self.pkt_max_len *cnt:self.pkt_max_len *cnt+self.pkt_max_len],self.dest)
			cnt += 1
		
		#probably not necessary anymore?
		if(len(data_tx[self.pkt_max_len *cnt:]) > 0):
			self.sock.sendto(data_tx[self.pkt_max_len *cnt:],self.dest)			
		
		return len(input_items[0])
