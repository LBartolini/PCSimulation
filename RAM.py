class RAM:
	def __init__(self):
        #ogni cella ha dimensione 1 byte
        #memoria con dimensione totale di 32 celle (32byte) di default.
		self.dim = 16
		self.Code = []
		self.Data = []
		for _ in range(self.dim):
			self.Code.append([0, 0, 0, 0, 0, 0, 0, 0])
			self.Data.append([0, 0, 0, 0, 0, 0, 0, 0])
    
	def ReadData(self, address):
		return (self.Data[address])

	def ReadCode(self, address):
		return (self.Code[address])

	def WriteCode(self, address, info = [0, 0, 0, 0, 0, 0, 0, 0]):
		self.Code[address] = info
	
	def WriteData(self, address, info = [0, 0, 0, 0, 0, 0, 0, 0]):
		self.Data[address] = info

	def Refresh(self):
		for i in range(self.dim):
			self.WriteCode(i)
			self.WriteData(i)
        
        