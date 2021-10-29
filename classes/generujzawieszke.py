import csv
from datetime import datetime

class GenerujZawieszke:
	def __init__(self, _lpath, lname, _lczasPracyDzwigu, _lczasPrzejazduDzwigu):
		self.tubs = []
		self.time = []
		self.name = str(lname)
		self.czasPracyDzwigu = _lczasPracyDzwigu
		self.czasPrzejazduDzwigu = _lczasPrzejazduDzwigu
		self.csv = {}
		self.offset = 0
		self.open(_lpath)
		

	def open(self, _lpath):
		_csv = []
		with open(_lpath) as csv_file:
			_csv_reader = csv.reader(csv_file, delimiter=',')

			# Odczytanie numeru programu i czasu startu zawieszki
			_rowt = next(_csv_reader)
			self.offset = int(_rowt[1])
			self.czasStartu = datetime.strptime(_rowt[0], '%d-%m-%Y %H:%M:%S')			
			# Jeśli ilosc powtorzeń wynosi zero, to ustaw jeden
			for row in _csv_reader:
				if (int(row[3]) == 0):
					_tmp = 1
				else:
					_tmp = int(row[3])

				# 0: wanna, 1: czas pracy, 2: obciek, 3: powtorzenia [900,10,1]
				self.csv[int(row[0])] = [int(row[1]), int(row[2]), int(row[3])]
				# Korekcja czasu pracy o czas pracy dźwigu i ilość powtorzeń [1, 930]
				_csv.append( [ int(row[0]), (int(row[1])+ self.czasPracyDzwigu + int(row[2])) * _tmp ] )

			# Generowanie listy tubes: [1, 1, 2, 2, 3, 3, 4, 4, ...]
			# Generowanie listy times: [0, 10, 13, 933, 936, 1556, ...]
			for row in _csv:
				if len(self.tubs)>0:
					_czas_przejazdu = (row[0]-self.tubs[-1])*self.czasPrzejazduDzwigu
					self.time.append( self.time[-1] + _czas_przejazdu)
					self.time.append( self.time[-1] + row[1])
					self.tubs.append( row[0] )
					self.tubs.append( row[0] )
				else: # Pierwsza wanna
					self.tubs.append(row[0])
					self.time.append(row[1] - self.czasPracyDzwigu)
					self.tubs.append(row[0])
					self.time.append(row[1])


	# Przesunięcie wszystkich czasów zawieszki o dany offset
	def move_right(self, loffset):
		for i in range(0, len(self.time)):
			self.time[i] += loffset	


	# Funkcja tworzy słownik. Klucz to numer wanny. Dwa argumenty [czas startu, czas konca] pracy
	# {1: [80, 90], 2: [93, 1013], 3: [1016, 1636], 4: [1639, 1719], ...}
	def get_dict(self, lopt = ''):		
		uniqe_tubs = list(sorted(set(self.tubs)))
		dic = {}
		for tub in uniqe_tubs:
			tmp = []
			for i in zip(self.tubs, self.time):
				if (i[0] == tub):
					tmp.append(i[1])
			if (lopt == 'A' and tub <= 18) or (lopt == 'B' and tub >= 19) or (lopt != 'A' and lopt != 'B'):
				dic[tub] = tmp
		return dic


	def get_rect(self, lopt, ltol):
		XX = []
		# ------- Wygenerowanie listy zakresow -------
		for i in list(zip(self.tubs, self.time)):
			if lopt == 'A':
				if i[0] <= 18:
					XX.append( i[1] )
			if lopt == 'B':
				if i[0] >= 19:
					XX.append( i[1] )	
		# --------
		_start = XX[0]
		_stop = 0
		tmp = []
		for i in range(0, len(XX)-1):
			if XX[i+1]-XX[i] <= ltol:
				_stop = XX[i+1]
			else:
				tmp.append( [_start, _stop+30] )
				_start = XX[i+1]
			if (i+1 == len(XX)-1):
				_stop = XX[-1]
				tmp.append( [_start, _stop] )
		if lopt == 'B':
			tmp.pop()
		return tmp


	'''	
	def get_tubs(self, lopt, lusun = False):
		if lopt == 'A':
			t = [tub for tub in self.tubs if tub <= 18]
		if lopt == 'B':
			t = [tub for tub in self.tubs if tub >= 19]
		if lusun == True:
			if t[-1] == t[-2]:
				t.pop()
		return t
	'''