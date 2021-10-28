#from operator import itemgetter

class App:

	def __init__(self, _ltolerancja):
		self.lista_zawieszek = []
#		self.tolerancja = ltolerancja
#		self.allTubs = []
#		self.allTime = []

	'''
	def liczba(self):
		return len(self.lista)


	def dodaj(self, lzawieszka):
		self.lista.append(lzawieszka)
		if self.liczba() > 1:
			self.przesun()


	def mergeDict(self, dict1, dict2):
		dict3 = {**dict2, **dict1}
		for key, value in dict3.items():
			if key in dict1 and key in dict2:
				dict3[key] = (value , dict2[key])
		return dict3


	def overlap(self, _la, _lb):
		return _la[1] >= _lb[0] and _lb[1] >= _la[0]


	def sumaPierwszychDict(self):
		di = {}
		for key in range(1,37):
			tmp = []
			for i in self.lista[:-1]:
				dic = i.get_dict()
				if key in dic.keys():
					tmp.append(dic[key])
			if len(tmp)>0:
				di[key] = tmp
		return di


	def sumaPierwszychRect(self, lopt):
		di = []
		for i in self.lista[:-1]:
			di += (i.get_rect(lopt, self.tolerancja))
		return di


	def checkCollisions(self, lopt):
		_ostatni = self.lista[-1].get_rect(lopt, self.tolerancja)
		_pierwsze = self.sumaPierwszychRect(lopt)
		kolizje = 0
		for x in _ostatni:
			for y in _pierwsze:
				if self.overlap(x,y):
					kolizje = y[1] - x[0]+3
					break
		return kolizje					


	def przesun(self):
		# -------- Przesunięcie zaraz za ostatni wykres --------
		offset = 0
		if self.lista[-1].time[0] <= self.lista[-2].time[0]:
			offset = (self.lista[-2].time[0] - self.lista[-1].time[0]) + self.tolerancja			
		self.lista[-1].move_right(offset)		

		# -------- Przesunięcie wanny --------
		offset = 0
		_ostatni = self.lista[-1].get_dict()
		_pierwsze = self.sumaPierwszychDict()
		_tubs_wspolne = sorted(set(_pierwsze).intersection(_ostatni))
		print('wspolne')
		print(_pierwsze)
		for tub in _tubs_wspolne:
			for val in _pierwsze[tub]:				
				if self.overlap(_ostatni[tub], val):
					offset = val[1] - _ostatni[tub][0]+1
					self.lista[-1].move_right(offset+self.tolerancja)
					_ostatni = self.lista[-1].get_dict()

		# -------- Przesunięcie przejazdu -------- 			
		offsetA = 1
		offsetB = 1
		self.lista[-1].move_right( int(self.lista[-1].przesuniecie) ) # Przesunięcie startu nowej zawieszki w zaleznosci od czasu, jaką już pracuje

		while (offsetA > 0) or (offsetB > 0):
			offsetA = self.checkCollisions('A')
			self.lista[-1].move_right(offsetA)	
			offsetB = self.checkCollisions('B')
			self.lista[-1].move_right(offsetB)			


	def rysuj_sciezke(self, lopt):
		plc = []
		program = []

		for k, i in enumerate(self.lista):
			for key, val in i.get_dict(lopt).items():
				if (key==1) or (key==19):
					str = 'pobierz'
				else:
					str = 'wsadz'
				plc.append([key, val[0], i.nazwa, str, i.csv[key][0], i.csv[key][1], i.csv[key][2] ])
				
				if key!=1 and key!=18 and key!=19 and key!=36:
					plc.append([key, val[1], i.nazwa, 'wyjmij', 0, 0, 0])
		plc = sorted(plc, key=itemgetter(1))

		program = list(plc)
		plc = list(zip(*plc))
		plc = [list(plc[0]), list(plc[1])]

		self.allTubs = list(plc[0])
		self.allTime = list(plc[1])
		
		if lopt == 'A':
			self.allTubs.append(1)
		if lopt == 'B':
			self.allTubs.append(19)
		self.allTime.append(self.allTime[-1] + ((self.allTubs[-2]-self.allTubs[-1])*3))	

		return program
	'''