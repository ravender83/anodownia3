import csv
from datetime import datetime

class GenerujZawieszke:
	def __init__(self, _lpath, _lczasPracyDzwigu, _lczasPrzejazduDzwigu):
		self.tubs = []
		self.time = []
		#self.czasStartu = 
		#self.przesuniecie = 0
		#self.csv = {}
		self.open(_lpath)

	def open(self, _lpath):
		_csv = []
		with open(_lpath) as csv_file:
			_csv_reader = csv.reader(csv_file, delimiter=',')

			# Odczytanie numeru programu i czasu startu zawieszki
			_rowt = next(_csv_reader)
			self.czasStartu = datetime.strdtime(_rowt[0], '%d-%m-%Y %H:%M:%S')

	'''
	def open(self, lpath):
		_csv = []
		with open(lpath) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			
			# Odczytanie numeru programu i czasu startu zawieszki
			rowt = next(csv_reader)
			self.numer_programu = rowt[0]
			self.dataStartu = rowt[1]
			self.czasStartu = rowt[2]
			self.przesuniecie = rowt[3]
			
			for row in csv_reader:
				if (int(row[3]) == 0):
					_tmp = 1
				else:
					_tmp = int(row[3])

				# Dodanie do programu czasu przejazdu dźwigu i czasu jego pracy np. [2, 930]
				self.csv[int(row[0])] = [int(row[1]), int(row[2]), int(row[3])]
				_csv.append( [ int(row[0]), (int(row[1])+self.czasPracyDzwigu+int(row[2]))*_tmp ] )

			for row in _csv:
				if len(self.tubs)>0:
					_czas_przejazdu = (row[0]-self.tubs[-1])*self.czasPrzejazduDzwigu
					self.time.append( self.time[-1] + _czas_przejazdu)
					self.time.append( self.time[-1] + row[1])
					self.tubs.append( row[0] )
					self.tubs.append( row[0] )
				else: # Pierwsza wanna
					self.tubs.append(row[0])
					self.time.append(row[1]-self.czasPracyDzwigu)
					self.tubs.append(row[0])
					self.time.append(row[1])

			# for key, value in self.csv.items():
			# 	print(key, '->', value)
	
	def move_right(self, loffset):
		for i in range(0, len(self.time)):
			self.time[i] += loffset


	def check_right(self, loffset):
		tmp = []
		for i in range(0, len(self.time)):
			tmp.append(self.time[i] + loffset)
		return tmp


	def get_len(self):
		return len(self.tubs)


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