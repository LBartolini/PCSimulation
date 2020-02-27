from MB import *

class IO:
	def __init__(self):
		self.Buffer = [0, 0, 0, 0, 0, 0, 0, 0]
	
	def Input(self):
		inp = input('Inserire numero in input.\n>>> ')
		self.Buffer = DTB(int(inp))

	def Output(self):
		print(BTD(self.Buffer), ':' ,self.Buffer)
		input("Premere INVIO per continuare...")

	def Refresh(self):
		self.Buffer = [0, 0, 0, 0, 0, 0, 0, 0]
