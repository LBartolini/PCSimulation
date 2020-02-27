#Math Binary

def Len(n):
	if ( n > 99 ):
		return 3
	elif ( 10 <= n <= 99):
		return 2
	elif ( 0 <= n < 10):
		return 1

def Scomp(n):
	num = n
	temp = [0, 0, 0]
	len = Len(num)
	while len != 0:
		x = 10**(len-1)
		temp[3 - len] = int(num / x)
		num = num % x
		len -= 1
	return temp

def DTB(n): # Decimal to Binary
	Ris = [0, 0, 0, 0, 0, 0, 0, 0]
	num = n
	i = 7
	while num != 0:
		Ris[i] = num % 2
		num = int(num / 2)
		i -= 1
	return Ris

def BTD(n, semi = False): # Binary to Decimal
	if not semi:
		Ris = 0
		for i, cNum in enumerate(n):
			index = 7 - i
			Ris += cNum * (2 ** index)
		return Ris
	else:
		Ris1 = 0
		Ris2 = 0
		for i in range(4):
			index = 3 - i
			Ris1 += n[i] * (2 ** index)
		for i in range(4, 8):
			index = 7 - i
			Ris2 += n[i] * (2 ** index)
		return Ris1, Ris2

def BinSum(n1, n2):
	if n1+n2 <= 255: return DTB(n1+n2)
	else: return [0, 0, 0, 0, 0, 0, 0, 0]

def BinSub(n1, n2):
	if n1-n2>= 0: return DTB(n1-n2), 1
	else: return [0, 0, 0, 0, 0, 0, 0, 0], 0