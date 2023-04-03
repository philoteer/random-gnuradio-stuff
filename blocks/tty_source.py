import sys
import time
import numpy as np
import serial
from gnuradio import gr

class blk(gr.sync_block):
	def __init__(self, tty_path = "/dev/ttyUSB0", baud=115200, tx_command='\r\nimport utils;utils.print_wav("recordings/test.wav")\r\n', rx_flush = True, init_sleep = 4.0): 
		gr.sync_block.__init__(
			self,
			name='tty source',   # will show up in GRC 
			in_sig=[],
			out_sig=[np.float32]
		) 
		
		self.serial = None
		self.tx_command = tx_command
		try:
			self.serial = serial.Serial( port=tty_path, baudrate=baud)			
			self.serial.timeout = 1.0
			print(self.serial.isOpen())
			
			if(rx_flush):
				print("### flush ###")
				self.serial.read(size=65535)
			time.sleep(init_sleep)
			if(rx_flush):
				print("### flush ###")
				self.serial.read(size=65535)
			self.serial.write(tx_command.encode())			
			#self.serial.timeout = 1.0
		except:
			print("No serial connection :(")
	def work(self, input_items, output_items):				
		#todo: check output_items length
		
		foo = self.serial.readline()
		try:
			if(len(foo) > 0):
				foo = foo.split()
				
				for i in range (0, len(foo)):
					output_items[0][i] = float(foo[i])
			return len(foo)

		except: #retry the connection
			print("retrying:")
			self.serial.read(size=65535)
			self.serial.write(self.tx_command.encode())			
			
		return 0
