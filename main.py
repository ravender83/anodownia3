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
folder = os.path.join(os.path.dirname(__file__), 'rav')
ext = 'rav'


def pri(zaw, u):
	ls = []
	ls.append('#-------------------------------------------------------')
	ls.append(f'tubs{u} = {zaw.lista[-1].tubs}')
	ls.append(f'time{u} = {zaw.lista[-1].time}')
	ls.append(f'rectA{u} = {zaw.lista[-1].get_rect("A", tolerancja)}')
	ls.append(f'rectB{u} = {zaw.lista[-1].get_rect("B", tolerancja)}')	
	ls.append(f'start{u} = "{zaw.lista[-1].czasStartu}"')
	ls.append(f'koniec{u} = "{zaw.lista[-1].czasKonca}"')

	for i in ls:
		print(i)
	return ls
	#print('#-------------------------------------------------------')
	#print(f'tubs{u} = {zaw.lista[-1].tubs}')
	#print(f'time{u} = {zaw.lista[-1].time}')
	#print(f'rectA{u} = {zaw.lista[-1].get_rect("A", tolerancja)}')
	#print(f'rectB{u} = {zaw.lista[-1].get_rect("B", tolerancja)}')	
	#print(f'start{u} = "{zaw.lista[-1].czasStartu}"')
	#print(f'koniec{u} = "{zaw.lista[-1].czasKonca}"')

#-------------------------------------------------------------------------
# Funkcja szuka plików csv o nazwie liczbowej. Nazwę każdego znalezionego pliku zapisuje
# do sortowanej listy. W przypadku znalezienia pliku 'new.csv' zapisuje w pierwszej linijce
# aktualny czas sterownika PLC i zmienia jego nazwę na największy możliwy numer
# return: list [1, 2, 5, 6, ...] - nazwy plików w folderze csv/
#-------------------------------------------------------------------------
def zapiszCzasCSV(_file, _dataczas, _offset, _czaskonca):
	sciezka = os.path.join(folder, f'{_file}.{ext}')
	with open(sciezka, 'r', newline='') as f:
		_lines = f.readlines()
	_lines[0] = f'{_dataczas}, {_offset}, {_czaskonca}\r\n'
	with open(sciezka, 'w', newline='') as f:			
		f.writelines(_lines)


def loadCSV(_pustaKolejka):
	if _pustaKolejka:
		sciezka = os.path.join(os.path.dirname(__file__), 'rav', '*.rav')
		for ravpath in glob.iglob(sciezka):
			os.remove(ravpath)

	_csvFiles = []
	_maxNr = 0
	sciezka = os.path.join(folder, f'*.{ext}')
	for file in glob.glob(sciezka):
		_filename = os.path.splitext(os.path.basename(file))[0]		
		if _filename.isdigit():
			_dig = int(_filename)
			if _dig > _maxNr:
				_maxNr = _dig
			_csvFiles.append( _dig )
	
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
	sciezka = os.path.join(folder, f'new.csv')
	sciezka2 = os.path.join(folder, f'{_maxNr+1}.{ext}')

	if os.path.isfile(sciezka):
		os.rename(sciezka, sciezka2)
		_csvFiles.append( int(_maxNr+1) )
	return sorted(_csvFiles)	


def generuj(_listaPlikowCSV, _dataczas):
	zawieszki = App(tolerancja)

	for plikCSV in _listaPlikowCSV:
		zawieszki.dodaj( GenerujZawieszke(f'{folder}/{plikCSV}.{ext}', plikCSV ,czas_pracy_dzwigu, czas_przejazdu_dzwigu, _dataczas))
		zapiszCzasCSV(plikCSV, zawieszki.lista[-1].czasStartu, zawieszki.lista[-1].offset, zawieszki.lista[-1].czasKonca)
		a = pri(zawieszki, plikCSV)
	
		sciezka = os.path.join(folder, 'pri.txt')
		textfile = open(sciezka, 'a')
		for element in a:
			textfile.write(element + "\n")
		textfile.close()

	# -------------------------- A ----------------------------
	A = zawieszki.generuj_sciezke('A')
	sciezka = os.path.join(folder, 'A.csv')
	with open(sciezka, 'w', newline='') as f:
		write = csv.writer(f)
		write.writerows(A)
	print(A)
	# -------------------------- B ----------------------------
	B = zawieszki.generuj_sciezke('B')
	sciezka = os.path.join(folder, 'B.csv')
	with open(sciezka, 'w', newline='') as f:
		write = csv.writer(f)
		write.writerows(B)
	print(B)
	s7plc = cQueue(A, B)


def main(argv):
	sciezka = os.path.join(folder, f'new.csv')
	
	if os.path.isfile(sciezka):		
		s7params = cPlcParams() #TODO: dodać wyjątek, jeśli nie pobrano parametrów

		if (s7params.PLCready == 1):
			listaPlikowCSV = loadCSV(s7params.pustaKolejka)
			generuj(listaPlikowCSV, s7params.actualtime)						
		else:
			print('Sterownik PLC nie jest gotowy do pracy...')
		
	else:
		print(f'Nie odnaleziono pliku new.csv')


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
