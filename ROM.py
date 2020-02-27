from MB import *

class ROM:
	def __init__(self):
        #ogni cella ha dimensione 1 byte
		self.dim = 16
		self.ISA = [] 
		for _ in range(self.dim):
			self.ISA.append([])
    
	def Read(self, address, index):
		return (self.ISA[address][index])

	def Write(self, address, info = []):
		self.ISA[address] = info

	def Refresh(self):
		for i in range(self.dim):
			self.Write(i)