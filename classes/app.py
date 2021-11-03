from datetime import datetime
from datetime import timedelta
from operator import itemgetter

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
				# gdy dodano nową zawieszkę
				_roznica = (self.lista[-1].czasStartu - self.lista[0].czasStartu).total_seconds()
				self.przesun(_roznica)
				self.lista[-1].offset = int(self.lista[-1].time[0])
				self.lista[-1].czasStartu = self.dodajsekundy(self.lista[0].czasStartu, int(self.lista[-1].offset))				
			else:
				self.lista[-1].move_right(self.lista[-1].offset)
		else:
			self.lista[-1].offset = 0
		self.lista[-1].czasKonca = self.dodajsekundy(self.lista[-1].czasStartu, self.lista[-1].time[-1] - self.lista[-1].time[0]+self.tolerancja)


	def przesun(self, offset=0):
		# -------- Przesunięcie zaraz za ostatni wykres --------
		self.lista[-1].move_right(offset+10)		
		
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


	def generuj_sciezke(self, lopt):
		plc = []
		program = []

		for key1, _zawieszka in enumerate(self.lista):
			for key2, val2 in _zawieszka.get_dict(lopt).items():
				if (key2==1) or (key2==19):
					_str = 'pobierz'
					_TXyear = _zawieszka.czasStartu.year
					_TXmonth = _zawieszka.czasStartu.month
					_TXday = _zawieszka.czasStartu.day
					_TXhour = _zawieszka.czasStartu.hour
					_TXminute = _zawieszka.czasStartu.minute
					_TXsecond = _zawieszka.czasStartu.second		
				else:
					_str = 'umiesc'
					_TXyear = 1970
					_TXmonth = 1
					_TXday = 1
					_TXhour = 0
					_TXminute = 0
					_TXsecond = 0

				_TXstart = int(val2[0])
				_TXkoniec = int(val2[1])
				_TXwanna = key2
				_TXname = _zawieszka.name
				_TXoperacja = _str
				_TXpraca = _zawieszka.csv[key2][0]
				_TXobciek = _zawieszka.csv[key2][1]
				_TXpowtorzenia = _zawieszka.csv[key2][2]
				
				plc.append([ _TXstart, _TXwanna, _TXname, _TXoperacja, _TXpraca, _TXobciek, _TXpowtorzenia, _TXyear, _TXmonth, _TXday, _TXhour, _TXminute, _TXsecond ])

				if key2!=1 and key2!=18 and key2!=19 and key2!=36:
					plc.append([ _TXkoniec, _TXwanna, _TXname, 'wyjmij', 0, 0, 0, 1970, 1, 1, 0, 0, 0])
		plc = sorted(plc, key=itemgetter(0))

		program = list(plc)
		return program


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