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

# CONFIG
czas_pracy_dzwigu = 10 # czas opuszczenia lub podnoszenia dzwigu
czas_przejazdu_dzwigu = 3 # czas przejazdu dzwigu nad jedna wanna
tolerancja = 70 + czas_pracy_dzwigu #ruchy dzwigu ponizej tej wartosci beda laczone razem


def pri(zaw, u):
	print('#-------------------------------------------------------')
	print(f'tubs{u} = {zaw.lista[-1].tubs}')
	print(f'time{u} = {zaw.lista[-1].time}')
	print(f'rectA{u} = {zaw.lista[-1].get_rect("A", tolerancja)}')
	print(f'rectB{u} = {zaw.lista[-1].get_rect("B", tolerancja)}')	

'''


def generuj(_s7params):
	zawieszki = App(tolerancja)
	# (lpath, lczasPracyDzwigu, lczasPrzejazduDzwigu)
	nowaZawieszka = GenerujZawieszke(f'prog/new.csv', 1, praca, przejazd)
	pri(nowaZawieszka)	

	# -------------------------- A ----------------------------
	A = zawieszki.generuj_sciezke(nowaZawieszka, _s7params.dataczas, 'A')
	with open('prog/A.csv', 'w', newline='') as f:
		write = csv.writer(f)
		write.writerows(A)
		f.close
	#print(A)

	# -------------------------- B ----------------------------
	B = zawieszki.generuj_sciezke(nowaZawieszka, _s7params.dataczas, 'B')
	with open('prog/B.csv', 'w', newline='') as f:
		write = csv.writer(f)
		write.writerows(B)
		f.close
	#print(B)	

	s7plc = cQueue(A, B)

'''

#-------------------------------------------------------------------------
# Funkcja szuka plików csv o nazwie liczbowej. Nazwę każdego znalezionego pliku zapisuje
# do sortowanej listy. W przypadku znalezienia pliku 'new.csv' zapisuje w pierwszej linijce
# aktualny czas sterownika PLC i zmienia jego nazwę na największy możliwy numer
# return: list [1, 2, 5, 6, ...] - nazwy plików w folderze csv/
#-------------------------------------------------------------------------

def zapiszCzasCSV(_file, _time):
	with open(f'csv/{_file}.csv', 'r', newline='') as f:
		_lines = f.readlines()
	f.close
	_lines[0] = _time.strftime('%d-%m-%Y %H:%M:%S\r\n')
	with open(f'csv/{_file}.csv', 'w', newline='') as f:			
		f.writelines(_lines)
	f.close


def loadCSV(_actualTime):
	_csvFiles = []
	_maxNr = 0

	for file in glob.glob('csv/*.csv'):
		if file[4:-4].isdigit():
			if int(file[4:-4]) > _maxNr:
				_maxNr = int(file[4:-4])
			_csvFiles.append( int(file[4:-4]) )

	# znaleziono nowy plik - ustawienie czasu PLC, zmiana nazwy
	if os.path.isfile('csv/new.csv'):
		zapiszCzasCSV('new', _actualTime)
		os.rename('csv/new.csv', f'csv/{_maxNr+1}.csv')
		_csvFiles.append( int(_maxNr+1) )
		#_csvFiles.append( 'new' )
	return sorted(_csvFiles)	


def generuj(_listaPlikowCSV, _dataczas):
	zawieszki = App(tolerancja)

	for plikCSV in _listaPlikowCSV:
		zawieszki.dodaj( GenerujZawieszke(f'csv/{plikCSV}.csv', czas_pracy_dzwigu, czas_przejazdu_dzwigu), _dataczas)
		pri(zawieszki, plikCSV)

	#_offset = zawieszki.lista[-1].time[0] # Offset startu nowej zawieszki w sekundach np. 2354
	#_czasstartu = zawieszki.lista[0].czasStartu + datetime.timedelta(0, _offset ) # Czas realny powiększony o offset
	#zapiszCzasCSV(plikCSV, _czasstartu)

	'''
	a = sorted(zawieszki.sumaWszystkichRect('A'))
	print('====', a)cl
	b = sorted(zawieszki.sumaWszystkichRect('B'))
	print('====', b)
	a1 = zawieszki.sumaWszystkichDict()
	print('====', a1)
	'''

def main(argv):
	if os.path.isfile('csv/new.csv'):		
		s7params = cPlcParams() #TODO: dodać wyjątek, jeśli nie pobrano parametrów

		if (s7params.PLCready == 1):
			listaPlikowCSV = loadCSV(s7params.dataczas)
			generuj(listaPlikowCSV, s7params.dataczas)						
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

