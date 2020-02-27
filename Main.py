from CPU import *
from RAM import *
from BUS import *
from ROM import *
from IO import *
from MB import *
import time, os

class PC:
    def __init__(self, automatic=True, vis = False):
        self.RAM = RAM()
        self.BUS = BUS()
        self.ROM = ROM()
        self.IO = IO()
        self.CPU = CPU()
        self.automatic = automatic
        self.on = True
        self.jmp = False
        self.greater = False
        self.vis = vis
        self.data = False

    def visPC(self): #visualize states inside PC
      for i in range(1000):
        print('\n')
      print('-----------------------------PC-----------------------------\n------------------------------------------------------------')
      self.BUS.Visualize()
      print('Registri:\nAX  : ', self.CPU.AX.Memory, '\nDX  : ', self.CPU.DX.Memory)
      print('\nMAR : ', self.CPU.MAR)
      print('IR  : ', self.CPU.IR, '\nPRC  : ', self.CPU.PRC, '\nSIC : ', self.CPU.SIC, '\nSIR : ', self.CPU.SIR)
      print('\nI/O:\nBuffer : ', self.IO.Buffer)
      print('\nRAM:\n')
      print('Code Segment:')
      for i in range(16):
        print(i, self.RAM.Code[i])
      print('\nData Segment:')
      for i in range(16):
        print(i, self.RAM.Data[i])
      if self.automatic:
        time.sleep(1)
      else:
        input("\n\nPremi INVIO per continuare...\n")


    def fillROM(self):
      self.ROM.Write(0, [])
      self.ROM.Write(1, [1])
      self.ROM.Write(2, [2, 3])
      self.ROM.Write(3, [2, 4])
      self.ROM.Write(4, [5, 0])
      self.ROM.Write(5, [6, 0])
      self.ROM.Write(6, [7])
      self.ROM.Write(7, [8, 9, 4])
      self.ROM.Write(8, [6, 10, 11])
      self.ROM.Write(9, [12])
      self.ROM.Write(10, [13])
      self.ROM.Write(11, [14])
      self.ROM.Write(12, [15])

    def updSI(self): #update sub instructions(main cycle of execute and decode)
      addr = BTD(self.CPU.IR, semi=True)[0]
      l = len(self.ROM.ISA[addr])
      self.CPU.SIC = 0
      if l == 0:
        self.on = False
        if self.vis: self.visPC()
      else:
        for _ in range(l):
          self.CPU.SIR = self.ROM.Read(addr, self.CPU.SIC)
          self.exeSI()
          if self.vis: self.visPC()
          self.CPU.SIC += 1


    def exeSI(self): #check sub instructions
      if self.CPU.SIR == 0:
        self.RAM.WriteData(BTD(self.CPU.IR, semi=True)[1], self.BUS.BUS)
      elif self.CPU.SIR == 1:
        self.CPU.AX.Write(BinSum(BTD(self.CPU.AX.Read()), BTD(self.CPU.DX.Read())))
      elif self.CPU.SIR == 2:
        self.BUS.BUS = self.RAM.ReadData(BTD(self.CPU.IR, semi=True)[1])
      elif self.CPU.SIR == 3:
        self.CPU.AX.Write(self.BUS.BUS)
      elif self.CPU.SIR == 4:
        self.CPU.DX.Write(self.BUS.BUS)
      elif self.CPU.SIR == 5:
        self.BUS.BUS = self.CPU.AX.Read()
      elif self.CPU.SIR == 6:
        self.BUS.BUS = self.CPU.DX.Read()
      elif self.CPU.SIR == 7:
        sub = BinSub(BTD(self.CPU.AX.Read()), BTD(self.CPU.DX.Read()))
        if BTD(self.CPU.IR, semi=True)[1] == 0:
          self.CPU.AX.Write(sub[0])
        elif BTD(self.CPU.IR, semi=True)[1] == 1:
          if sub[1] == 0:
            self.greater = False
          else:
            self.greater = True
      elif self.CPU.SIR == 8:
        self.IO.Input()
      elif self.CPU.SIR == 9:
        self.BUS.BUS = self.IO.Buffer
      elif self.CPU.SIR == 10:
        self.IO.Buffer = self.BUS.BUS
      elif self.CPU.SIR == 11:
        self.IO.Output()
      elif self.CPU.SIR == 12:
        self.CPU.PRC = BTD(self.CPU.IR, semi=True)[1]
        self.jmp = True
      elif self.CPU.SIR == 13:
        if BTD(self.CPU.AX.Read())==0:
          self.CPU.PRC = BTD(self.CPU.IR, semi=True)[1]
          self.jmp = True
      elif self.CPU.SIR == 14:
        if self.greater:
          self.CPU.PRC = BTD(self.CPU.IR, semi=True)[1]
          self.jmp = True
      elif self.CPU.SIR == 15:
        temp = self.CPU.AX.Read()
        self.CPU.AX.Write(self.CPU.DX.Read())
        self.CPU.DX.Write(temp)

      
    def StartUp(self): #Ciclo Macchina
      self.fillROM()
      while self.on:
        self.jmp = False
        self.BUS.BUS = self.RAM.ReadCode(self.CPU.PRC)   
        if self.vis: self.visPC()
        self.CPU.IR = self.BUS.BUS
        self.CPU.MAR = self.CPU.IR[4:]
        self.updSI()
        self.visPC()
        if not self.jmp: self.CPU.PRC += 1
        self.IO.Refresh()
        self.BUS.Refresh()  
    
    def SetCode(self):
      while True:
        print('\n\n')
        cd = input("1. Code\n2. Data\n3. Carica programma\n4. Esegui Programma\n>>> ") #choose for code or data
        if cd == '1':
          pos = input("Posizione in memoria (decimale 0-15)\n>>> ") #per puntare la memoria
          self.RAM.WriteCode(int(pos), self.GetCode(pos, cd))
        elif cd == '2':
          pos = input("Posizione in memoria (decimale 0-15)\n>>> ") #per puntare la memoria
          self.RAM.WriteData(int(pos), self.GetCode(pos, cd))
        elif cd == '3':
          THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
          my_file = os.path.join(THIS_FOLDER, 'Code.txt')
          lines = [line.rstrip('\n') for line in open(my_file)]
          for j, i in enumerate(lines):
            if not self.data:
              if i[:3] == '.DT': self.data = True
              else: self.RAM.WriteCode(j, self.LoadCode(i))
            else:
              pos = [0, 0, 0, 0, 0, 0, 0, 0]
              y = 4
              for k in range(4):
                pos[y] = int(i[k])
                y += 1
              pos = BTD(pos)
              data = i[5:13]
              self.RAM.WriteData(pos, self.LoadData(data))
        elif cd == '4':
          self.StartUp()
          break
        else:
          continue

    def LoadCode(self, txt):
      code_int = [0, 0, 0, 0, 0, 0, 0, 0]
      instr = txt[:3]
      x = 0
      op = txt[4:8]
      if instr == 'ADD':
        code_int[:4] = [0, 0, 0, 1]
      elif instr == 'LAX':
        code_int[:4] = [0, 0, 1, 0]
      elif instr == 'LDX':
        code_int[:4] = [0, 0, 1, 1]
      elif instr == 'MAX':
        code_int[:4] = [0, 1, 0, 0]
      elif instr == 'MDX':
        code_int[:4] = [0, 1, 0, 1]
      elif instr == 'SUB':
        code_int[:4] = [0, 1, 1, 0]
      elif instr == 'INN':
        code_int[:4] = [0, 1, 1, 1]
      elif instr == 'OUT':
        code_int[:4] = [1, 0, 0, 0]
      elif instr == 'JMP':
        code_int[:4] = [1, 0, 0, 1]
      elif instr == 'JMZ':
        code_int[:4] = [1, 0, 1, 0]
      elif instr == 'JMG':
        code_int[:4] = [1, 0, 1, 1]
      elif instr == 'SWC':
        code_int[:4] = [1, 1, 0, 0]
      for i in range(4, 8):
        code_int[i] = int(op[x])
        x += 1
      return code_int

    def GetCode(self, pos, cd):
      print('Posizione in Memoria  -> ', pos)
      code_txt = input("Codice -> ")
      code_int = [0, 0, 0, 0, 0, 0, 0, 0]
      if cd == '1':
        instr = code_txt[:3]
        x = 0
        op = code_txt[4:8]
        if instr == 'ADD':
          code_int[:4] = [0, 0, 0, 1]
        elif instr == 'LAX':
          code_int[:4] = [0, 0, 1, 0]
        elif instr == 'LDX':
          code_int[:4] = [0, 0, 1, 1]
        elif instr == 'MAX':
          code_int[:4] = [0, 1, 0, 0]
        elif instr == 'MDX':
          code_int[:4] = [0, 1, 0, 1]
        elif instr == 'SUB':
          code_int[:4] = [0, 1, 1, 0]
        elif instr == 'INN':
          code_int[:4] = [0, 1, 1, 1]
        elif instr == 'OUT':
          code_int[:4] = [1, 0, 0, 0]
        elif instr == 'JMP':
          code_int[:4] = [1, 0, 0, 1]
        elif instr == 'JMZ':
          code_int[:4] = [1, 0, 1, 0]
        elif instr == 'JMG':
          code_int[:4] = [1, 0, 1, 1]
        elif instr == 'SWC':
          code_int[:4] = [1, 1, 0, 0]
        for i in range(4, 8):
          code_int[i] = int(op[x])
          x += 1
      else:
        for i in range(8):
          code_int[i] = int(code_txt[i])
      return code_int

    def LoadData(self, txt):
      code_int = [0, 0, 0, 0, 0, 0, 0, 0]
      for i in range(8):
          code_int[i] = int(txt[i])
      return code_int

PC = PC(automatic=False, vis=False)
PC.SetCode()