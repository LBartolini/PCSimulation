from MB import *

class CPU:
	def __init__(self):
		self.AX = Register() 						# Calcoli matematici
		self.DX = Register() 						# Data input/output
		self.PRC = 0         						# Program Counter
		self.IR = [0, 0, 0, 0, 0, 0, 0, 0]          # Instruction Register
		self.MAR = [0, 0, 0, 0]
		self.SIC = 0         						# Sub Instruction Counter
		self.SIR = 0         						# Sub Instruction Register


class Register:
	def __init__(self):
		self.Memory = []
		for _ in range(8):
			self.Memory.append(0)
	
	def Read(self):
		return (self.Memory)

	def Write(self, info = [0, 0, 0, 0, 0, 0, 0, 0]):
		self.Memory = info

