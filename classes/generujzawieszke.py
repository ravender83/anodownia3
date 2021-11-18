import csv
from datetime import datetime

class GenerujZawieszke:
	def __init__(self, _lpath, lname, _lczasPracyDzwigu, _lczasPrzejazduDzwigu, _dataczas):
		self.tubs = []
		self.time = []
		self.name = lname
		self.czasPracyDzwigu = _lczasPracyDzwigu
		self.czasPrzejazduDzwigu = _lczasPrzejazduDzwigu
		self.csv = {}
		self.czasStartu = _dataczas
		self.czasKonca = _dataczas

		self.open(_lpath, _dataczas)
		

	def open(self, _lpath, _dataczas):
		_csv = []
		with open(_lpath) as csv_file:
			_csv_reader = csv.reader(csv_file, delimiter=',')

			# Odczytanie numeru programu i czasu startu zawieszki
			_rowt = next(_csv_reader)
			self.offset = int(_rowt[1].strip())

			if self.offset == -1:
				self.czasStartu = _dataczas
				self.czasKonca = _dataczas
			else:
				self.czasStartu = datetime.strptime(_rowt[0].strip(), '%Y-%m-%d %H:%M:%S')	
				self.czasKonca =  datetime.strptime(_rowt[2].strip(), '%Y-%m-%d %H:%M:%S')	

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
					self.time.append( int(self.time[-1] + _czas_przejazdu) )
					self.time.append( int(self.time[-1] + row[1]) )
					self.tubs.append( row[0] )
					self.tubs.append( row[0] )
				else: # Pierwsza wanna
					self.tubs.append(row[0])
					self.time.append( int(row[1] - self.czasPracyDzwigu) )
					self.tubs.append(row[0])
					self.time.append(int(row[1]) )
		csv_file.close()


	# Przesunięcie wszystkich czasów zawieszki o dany offset
	def move_right(self, loffset):
		for i in range(0, len(self.time)):
			self.time[i] += int(loffset)


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
		# tubs1 = [1, 1, 2, 2, 3, 3, 4, 4, 7, 7, 8, 8, 14, 14, 18, 18, 19, 19, 22, 22, 28, 28, 29, 29, 36, 36]
		# time1 = [0, 3, 4, 28, 29, 38, 39, 48, 51, 75, 76, 85, 91, 125, 129, 138, 139, 148, 151, 175, 181, 190, 191, 215, 222, 236]
		# ------- Wygenerowanie listy zakresow -------
		for i in list(zip(self.tubs, self.time)):
			if lopt == 'A':
				if i[0] <= 18:
					XX.append( i[1] )
			if lopt == 'B':
				if i[0] >= 19:
					XX.append( i[1] )	
		XX.pop()
		XX.pop(0)
		# Generuję listę par zakresów
		# [3, 4, 28, 29, 38, 39, 48, 51, 75, 76, 85, 91, 125, 129]
		it = iter(XX)
		_pary = list(zip(it,it))
		# [(3, 4), (28, 29), (38, 39), (48, 51), (75, 76), (85, 91), (125, 129)]

		# Tworzę nową listę i dodaję do zakresów tolerancję
		_paryTol = []
		for i in _pary:
			_paryTol.append([i[0], i[1]+ltol])
		# Przykładowo dla ltol = 30
		# [[3, 34], [28, 59], [38, 69], [48, 81], [75, 106], [85, 121], [125, 159]]

		_tmp = [_paryTol[0]]
		for i in range(1, len(_paryTol)):
			if _paryTol[i][0] <= _tmp[-1][1]:
				_tmp[-1][1] = _paryTol[i][1]
			else:
				_tmp.append(_paryTol[i])
		return _tmp
