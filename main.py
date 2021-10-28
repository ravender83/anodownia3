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


def wypisz(_s7params, _listaPlikowCSV):
	print('')
	print('s7params.dataczas: ', _s7params.dataczas)
	print('s7params.PLCready: ', _s7params.PLCready)
	print('listaPlikowCSV: ', _listaPlikowCSV)
	print('')


'''

def pri(zaw):
	print('#-------------------------------------------------------')
	_u = 1
	print(f'tubs{_u} = {zaw.tubs}')
	print(f'time{_u} = {zaw.time}')
	print(f'rectA{_u} = {zaw.get_rect("A", tolerancja)}')
	print(f'rectB{_u} = {zaw.get_rect("B", tolerancja)}')	


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
		with open('csv/new.csv', 'r', newline='') as f:
			_lines = f.readlines()
		f.close
		_lines[0] = _actualTime.strftime('%d-%m-%Y %H:%M:%S\r\n')
		with open('csv/new.csv', 'w', newline='') as f:			
			f.writelines(_lines)
		f.close
		os.rename('csv/new.csv', f'csv/{_maxNr+1}.csv')
		_csvFiles.append( int(_maxNr+1) )
	return sorted(_csvFiles)	


def generuj(_listaPlikowCSV):
	zawieszki = App(tolerancja)

	for plikCSV in _listaPlikowCSV:
		#zawieszki.dodaj( GenerujZawieszke(f'csv/{plikCSV}.csv', czas_pracy_dzwigu, czas_przejazdu_dzwigu) )
		GenerujZawieszke(f'csv/{plikCSV}.csv', czas_pracy_dzwigu, czas_przejazdu_dzwigu)


def main(argv):
	if os.path.isfile('csv/new.csv'):		
		s7params = cPlcParams() #TODO: dodać wyjątek, jeśli nie pobrano parametrów

		if (s7params.PLCready == 1):
			listaPlikowCSV = loadCSV(s7params.dataczas)
			generuj(listaPlikowCSV)
		# 	if (s7params.check_if_empty()): # Jeśli sterownik nie wykonuje żadnego programu, tworzymy nowy program
		# 		#generuj(s7params)
		# 		pass
		# 	else: # Jeśli sterownik wykonuje program, dopisujemy nowe rozkazy
			pass
		else:
			print('Sterownik PLC nie jest gotowy do pracy...')
		
		wypisz(s7params, listaPlikowCSV)
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
