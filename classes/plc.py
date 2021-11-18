import snap7.client as c
from snap7.util import *
from snap7.types import *
import datetime
import struct

class cQueue:
    def __init__(self, _trackA, _trackB): 
        self.listProgram = []
        self.cProgramLen = 38 #from PLC - dlugosc cProgram
        self.listProgramAStart = 2 #from PLC TXRX A_krok
        self.listProgramBStart = 6844 #from PLC TXRX B_krok
        self.listProgramDB = 1 #from PLC TXRX     

        con = c.Client()
        res = con.connect('10.10.10.13', 0, 1)

        _trackAbytes = bytearray()
        for i in _trackA:
            _a = i[1].to_bytes(2, byteorder='big') # wanna
            _y0 = i[7].to_bytes(2, byteorder='big') # rok
            _y1 = i[8].to_bytes(1, 'big') # miesiac
            _y2 = i[9].to_bytes(1, 'big') # dzien
            _y3 = (0).to_bytes(1, 'big') # weekday
            _y4 = i[10].to_bytes(1, 'big') # godzina
            _y5 = i[11].to_bytes(1, 'big') # minuta
            _y6 = i[12].to_bytes(1, 'big') # sekunda
            _y7 = (0).to_bytes(4, 'big') # ms
            _b = i[2].to_bytes(2, 'big') # zawieszka
            _c = (10).to_bytes(1, 'big') # ...empty...
            _d = i[3].ljust(10).encode()
            _e = i[4].to_bytes(2, 'big') # tpraca
            _f = i[5].to_bytes(2, 'big') # tobciek
            _g = i[6].to_bytes(2, 'big') # tpowtorzenia
            _h = i[0].to_bytes(4, 'big') # offset
            _trackAbytes.extend(_a+ _y0+_y1+_y2+_y3+_y4+_y5+_y6+_y7+ _b+ _c + _c + _d+ _e+ _f+ _g+_h)

        _trackBbytes = bytearray()
        _off = _trackB[0][0]
        for i in _trackB:
            _a = i[1].to_bytes(2, byteorder='big') # wanna
            _y0 = i[7].to_bytes(2, byteorder='big') # rok
            _y1 = i[8].to_bytes(1, 'big') # miesiac
            _y2 = i[9].to_bytes(1, 'big') # dzien
            _y3 = (0).to_bytes(1, 'big') # weekday
            _y4 = i[10].to_bytes(1, 'big') # godzina
            _y5 = i[11].to_bytes(1, 'big') # minuta
            _y6 = i[12].to_bytes(1, 'big') # sekunda
            _y7 = (0).to_bytes(4, 'big') # ms
            _b = i[2].to_bytes(2, 'big') # zawieszka
            _c = (10).to_bytes(1, 'big') # ...empty...
            _d = i[3].ljust(10).encode()
            _e = i[4].to_bytes(2, 'big') # tpraca
            _f = i[5].to_bytes(2, 'big') # tobciek
            _g = i[6].to_bytes(2, 'big') # tpowtorzenia
            _h = (i[0]-_off).to_bytes(4, 'big') # offset
            _trackBbytes.extend(_a+ _y0+_y1+_y2+_y3+_y4+_y5+_y6+_y7+ _b+ _c + _c + _d+ _e+ _f+ _g+_h)

        con.write_area(Areas['DB'], self.listProgramDB, self.listProgramAStart, _trackAbytes)
        con.write_area(Areas['DB'], self.listProgramDB, self.listProgramBStart, _trackBbytes)
        con.write_area(Areas['DB'], self.listProgramDB, self.listProgramAStart-2, (len(_trackA)).to_bytes(2, 'big'))
        con.write_area(Areas['DB'], self.listProgramDB, self.listProgramBStart-2, (len(_trackB)).to_bytes(2, 'big'))
        con.disconnect()

#-------------------------------------------------------------------------
# Funkcja pobiera dane ze sterownika PLC
# self.dataczas - Aktualny czas na sterowniku PLC: 2021-10-28 13:30:58
# self.PLCready - Sygnał gotowości sterownika PLC: 0 / 1
#-------------------------------------------------------------------------
class cPlcParams:
    def __init__(self): 
        _listProgramStart = 13684 #from PLC TXRX.cPlcParams
        _listProgramDB = 1 #from PLC TXRX

        con = c.Client()
        res = con.connect('10.10.10.13', 0, 1)
        datas = con.read_area(Areas['DB'], _listProgramDB, _listProgramStart, 16)
        _year = int(struct.unpack('>h', datas[0:2])[0])
        _month = int(struct.unpack('B', datas[2:3])[0])
        _day = int(struct.unpack('B', datas[3:4])[0])
        _hour = int(struct.unpack('B', datas[5:6])[0])
        _minute = int(struct.unpack('B', datas[6:7])[0])
        _second = int(struct.unpack('B', datas[7:8])[0])
        self.PLCready = int(struct.unpack('>h', datas[12:14])[0])
        self.pustaKolejka = int(struct.unpack('>h', datas[14:16])[0])

        self.actualtime = datetime.datetime(_year, _month, _day, _hour, _minute, _second)

        con.disconnect()
    '''
    def check_if_empty(self):
        return ((self.Acount == 0) and (self.Bcount == 0))   
    '''       
