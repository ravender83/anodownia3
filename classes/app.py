from datetime import datetime
from datetime import timedelta

class App:

	def __init__(self, _ltolerancja):
		self.lista = []
		self.tolerancja = _ltolerancja


	def dodajsekundy(self, _czas, _sek):
		_b = _czas + timedelta(0,_sek)
		return _b


	# Dodanie zawieszki do listy zawieszek
	def dodaj(self, _lzawieszka):
		self.lista.append(_lzawieszka)		
		if len(self.lista) > 1:
			if (self.lista[-1].offset == -1):
				_roznica = (self.lista[-1].czasStartu - self.lista[0].czasStartu).total_seconds()
				self.przesun(_roznica)
				self.lista[-1].offset = int(self.lista[-1].time[0])
				self.lista[-1].czasStartu = self.dodajsekundy(self.lista[0].czasStartu, int(self.lista[-1].offset))
			else:
				self.lista[-1].move_right(self.lista[-1].offset)
		else:
			self.lista[-1].offset = 0
		

	def przesun(self, offset=0):
		# -------- Przesunięcie zaraz za ostatni wykres --------
		self.lista[-1].move_right(offset+self.tolerancja)		
		
		# -------- Przesunięcie wanny --------
		offset = 0
		_ostatni = self.lista[-1].get_dict()
		# {1: [[0, 10], [2928, 2938]], 2: [[13, 933], [2941, 3861]], ...}
		_pierwsze = self.sumaPierwszychDict()
		# _tubs_wspolne - Tworzy listę z numerami wanien, które są wspólne dla zawieszek istniejących
		# [1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 16, 17, ...]
		_tubs_wspolne = sorted(set(_pierwsze).intersection(_ostatni))

		for tub in _tubs_wspolne:
			for val in _pierwsze[tub]:				
				if self.overlap(_ostatni[tub], val):
					offset = val[1] - _ostatni[tub][0]+1
					self.lista[-1].move_right(offset+self.tolerancja)
					_ostatni = self.lista[-1].get_dict()
		
		# -------- Przesunięcie przejazdu -------- 			
		offsetA = 1
		offsetB = 1

		while (offsetA > 0) or (offsetB > 0):
			offsetA = self.checkCollisions('A')
			self.lista[-1].move_right(offsetA)	
			offsetB = self.checkCollisions('B')
			self.lista[-1].move_right(offsetB)	


	def overlap(self, _la, _lb):
		return _la[1] >= _lb[0] and _lb[1] >= _la[0]
	

	def sumaPierwszychRect(self, lopt):
		di = []
		for i in self.lista[:-1]:
			di += (i.get_rect(lopt, self.tolerancja))
		return di


	def sumaWszystkichRect(self, lopt):
		di = []
		for i in self.lista:
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

	'''
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

	# Funkcja tworzy słownik zawierający sumę zakresów wszystkich zawieszek aktualnie wykonywanych
	# {1: [[0, 10], [80, 90]], 2: [[13, 933], [93, 1013]], 3: [[936, 1556], [1016, 1636]], 4: [[1559, 1639], [1639, 1719]],...}
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

	def sumaWszystkichDict(self):
		di = {}
		for key in range(1,37):
			tmp = []
			for i in self.lista:
				dic = i.get_dict()
				if key in dic.keys():
					tmp.append(dic[key])
			if len(tmp)>0:
				di[key] = tmp
		return di		