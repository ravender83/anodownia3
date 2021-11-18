#-------------------------------------------
#	Description:	Anodownia 3
#	Version:		v1.0
#	Author:			Piotr Ślęzak
#	
#	Change log:
#		v1.0:		Anoda generated
#-------------------------------------------
from classes.plc import *
from classes.app import App
from classes.generujzawieszke import GenerujZawieszke 
import os
import glob
import csv

# CONFIG
'''
czas_pracy_dzwigu = 10 # czas opuszczenia lub podnoszenia dzwigu
czas_przejazdu_dzwigu = 3 # czas przejazdu dzwigu nad jedna wanna
tolerancja = 70 + czas_pracy_dzwigu #ruchy dzwigu ponizej tej wartosci beda laczone razem
'''
czas_pracy_dzwigu = 4 # czas opuszczenia lub podnoszenia dzwigu
czas_przejazdu_dzwigu = 1 # czas przejazdu dzwigu nad jedna wanna
tolerancja = 3 + czas_pracy_dzwigu #ruchy dzwigu ponizej tej wartosci beda laczone razem


def pri(zaw, u):
	print('#-------------------------------------------------------')
	print(f'tubs{u} = {zaw.lista[-1].tubs}')
	print(f'time{u} = {zaw.lista[-1].time}')
	print(f'rectA{u} = {zaw.lista[-1].get_rect("A", tolerancja)}')
	print(f'rectB{u} = {zaw.lista[-1].get_rect("B", tolerancja)}')	
	print(f'start{u} = "{zaw.lista[-1].czasStartu}"')
	print(f'koniec{u} = "{zaw.lista[-1].czasKonca}"')

#-------------------------------------------------------------------------
# Funkcja szuka plików csv o nazwie liczbowej. Nazwę każdego znalezionego pliku zapisuje
# do sortowanej listy. W przypadku znalezienia pliku 'new.csv' zapisuje w pierwszej linijce
# aktualny czas sterownika PLC i zmienia jego nazwę na największy możliwy numer
# return: list [1, 2, 5, 6, ...] - nazwy plików w folderze csv/
#-------------------------------------------------------------------------
def zapiszCzasCSV(_file, _dataczas, _offset, _czaskonca):
	with open(f'csv/{_file}.csv', 'r', newline='') as f:
		_lines = f.readlines()
	_lines[0] = f'{_dataczas}, {_offset}, {_czaskonca}\r\n'
	with open(f'csv/{_file}.csv', 'w', newline='') as f:			
		f.writelines(_lines)


def loadCSV():
	_csvFiles = []
	_maxNr = 0

	for file in glob.glob('csv/*.csv'):
		if file[4:-4].isdigit():
			if int(file[4:-4]) > _maxNr:
				_maxNr = int(file[4:-4])
			_csvFiles.append( int(file[4:-4]) )

	''' Usuwanie plikow, ktore zostały ukończone. Niestety uszkadza to offset
	_csvFilesTemp = _csvFiles[:]
	for _file in _csvFiles:
		with open(f'csv/{_file}.csv') as csv_file:
			_csv_reader = csv.reader(csv_file, delimiter=',')
			_rowt = next(_csv_reader)
			if int(_rowt[1].strip()) != -1:
				_czasKonca = datetime.strptime(_rowt[2].strip(), '%Y-%m-%d %H:%M:%S')
				#if _dataczas > _czasKonca:
				#	_csvFilesTemp.remove(_file)
		csv_file.close
	_csvFiles = _csvFilesTemp[:]
	'''

	# znaleziono nowy plik - ustawienie czasu PLC, zmiana nazwy
	if os.path.isfile('csv/new.csv'):
		os.rename('csv/new.csv', f'csv/{_maxNr+1}.csv')
		_csvFiles.append( int(_maxNr+1) )
	return sorted(_csvFiles)	


def generuj(_listaPlikowCSV, _dataczas):
	zawieszki = App(tolerancja)

	for plikCSV in _listaPlikowCSV:
		zawieszki.dodaj( GenerujZawieszke(f'csv/{plikCSV}.csv', plikCSV ,czas_pracy_dzwigu, czas_przejazdu_dzwigu, _dataczas))
		zapiszCzasCSV(plikCSV, zawieszki.lista[-1].czasStartu, zawieszki.lista[-1].offset, zawieszki.lista[-1].czasKonca)
		pri(zawieszki, plikCSV)

	# -------------------------- A ----------------------------
	A = zawieszki.generuj_sciezke('A')
	with open('csv/A.csv', 'w', newline='') as f:
		write = csv.writer(f)
		write.writerows(A)
	print(A)
	# -------------------------- B ----------------------------
	B = zawieszki.generuj_sciezke('B')
	with open('csv/B.csv', 'w', newline='') as f:
		write = csv.writer(f)
		write.writerows(B)
	print(B)
	s7plc = cQueue(A, B)	


def main(argv):
	if os.path.isfile('csv/new.csv'):		
		s7params = cPlcParams() #TODO: dodać wyjątek, jeśli nie pobrano parametrów

		if (s7params.PLCready == 1):
			listaPlikowCSV = loadCSV()
			generuj(listaPlikowCSV, s7params.actualtime)						
		else:
			print('Sterownik PLC nie jest gotowy do pracy...')
		
	else:
		print('Nie odnaleziono pliku prog/new.csv')


if __name__ == "__main__":
	try: 
		print('')
		print('>>>>>>>>>>>>>>> Start <<<<<<<<<<<<<<<')
		print('')
		main(1)
		print('')
		print('>>>>>>>>>>>>>>> Koniec <<<<<<<<<<<<<<<')
		print('')
	except:
		pass
