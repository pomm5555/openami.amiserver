# -*- coding: utf-8 -*-


import time
import PlugInsSupport.avrBridgePy as avrBridgePy



mega = avrBridgePy.avrBridge()


# PC0 - DB4
# PC1 - DB5
# PC2 - DB6
# PC3 - DB7
# PC4 - RS
# PC5 - E

PORT = 1

DB4 = 0
DB5 = 1
DB6 = 2
DB7 = 3
RS  = 4
E   = 5

         
def command(list):
    for elem in list:
        #print elem[0], elem[1]
        mega.setPortPin(PORT, elem[0], elem[1])

def enable():
    command(((E, 1),))
    #time.sleep(0.01)
    command(((E, 0),))

def lcd_init4bit():
    command(((E, 0), (RS, 0), (DB7, 0), (DB6, 0), (DB5, 1), (DB4, 1)))
    enable()
    #time.sleep(0.01*5)
    enable()
    #time.sleep(0.01*5)
    enable()
    command(((DB4, 0),))
    command(((E, 0), (RS, 0), (DB7, 0), (DB6, 0), (DB5, 1), (DB4, 0)))
    enable()
    #time.sleep(0.01*5)

#Konfiguration: 0b001dnfxx
#Einstellen der Interface Art, Modus, Font
#d = 0, 4-Bit Interface
#d = 1, 8-Bit Interface
#n = 0, 1 zeilig
#n = 1, 2 zeilig
#f = 0, 5x7 Pixel
#f = 1, 5x11 Pixel

def lcd_2zeilen():
    lcd_command("00101100")


#On/off control: 0b00001dcb
#Display insgesamt ein/ausschalten; den Cursor ein/ausschalten; den Cursor auf blinken schalten/blinken aus. Wenn das Display ausgeschaltet wird, geht der Inhalt des Displays nicht verloren. Der vorher angezeigte Text wird nach wiedereinschalten erneut angezeigt. Ist der Cursor eingeschaltet, aber Blinken ausgeschaltet, so wird der Cursor als Cursorzeile in Pixelzeile 8 dargestellt. Ist Blinken eingeschaltet, wird der Cursor als blinkendes ausgefülltes Rechteck dargestellt, welches abwechselnd mit dem Buchstaben an dieser Stelle angezeigt wird.
#d = 0, Display aus
#d = 1, Display ein
#c = 0, Cursor aus
#c = 1, Cursor ein
#b = 0, Cursor blinken aus
#b = 1, Cursor blinken ein
def lcd_dispon():
    lcd_command("00001111")

#Entry mode: 0b000001is
#Legt die Cursor Richtung sowie eine mögliche Verschiebung des Displays fest
#i = 1, Cursorposition bei Ausgabe eines Zeichens erhöhen
#i = 0, Cursorposition bei Ausgabe eines Zeichens vermindern
#s = 1, Display wird gescrollt, wenn der Cursor das Ende/Anfang, je nach Einstellung von i, erreicht hat.
def lcd_noscroll():
    lcd_command("00000110")
    

def lcd_clear():
    lcd_command("00000001")
    #time.sleep(0.01*5)

def lcd_data(byte):
    mega.setPortPin(PORT, RS, 1)
    mega.setPortPin(PORT, DB7, int(byte[0]))
    mega.setPortPin(PORT, DB6, int(byte[1]))
    mega.setPortPin(PORT, DB5, int(byte[2]))
    mega.setPortPin(PORT, DB4, int(byte[3]))
    enable()
    mega.setPortPin(PORT, DB7, int(byte[4]))
    mega.setPortPin(PORT, DB6, int(byte[5]))
    mega.setPortPin(PORT, DB5, int(byte[6]))
    mega.setPortPin(PORT, DB4, int(byte[7]))
    enable()
    #time.sleep(0.01*5)

def lcd_command(byte):
    mega.setPortPin(PORT, RS, 0)
    mega.setPortPin(PORT, DB7, int(byte[0]))
    mega.setPortPin(PORT, DB6, int(byte[1]))
    mega.setPortPin(PORT, DB5, int(byte[2]))
    mega.setPortPin(PORT, DB4, int(byte[3]))
    enable()
    mega.setPortPin(PORT, DB7, int(byte[4]))
    mega.setPortPin(PORT, DB6, int(byte[5]))
    mega.setPortPin(PORT, DB5, int(byte[6]))
    mega.setPortPin(PORT, DB4, int(byte[7]))
    enable()



def lcd_data_string(string):
    for elem in string:
        lcd_data(char2bin(elem))

def init_lcd():
    lcd_init4bit()
    lcd_2zeilen()
    lcd_dispon()
    lcd_noscroll()



def fill(string, size):
    rest = size-string.__len__()
    for i in range(0, rest):
        string='0'+string
    return string

def char2bin(c):
    c = ord(c)
    i=c
    result = ""
    while not i == 0:
        result = str(i%2)+result
        i = i/2
    return fill(result, 8)

init_lcd()
lcd_clear()
lcd_data_string("zeile1einfa\nchmaldrueberschreiben")
#lcd_command("00000010")
#lcd_command("00011100")

lcd_data_string("zeile2")
#lcd_dataA()
#lcd_dataB()

