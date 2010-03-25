# -*- coding: utf-8 -*-
import time
import avrBridgePy as avrBridgePy


class lcd:

    # PC0 - DB4
    # PC1 - DB5
    # PC2 - DB6
    # PC3 - DB7
    # PC4 - RS
    # PC5 - E

    def __init__(self):

        self.PORT = 1
        self.DB4 = 0
        self.DB5 = 1
        self.DB6 = 2
        self.DB7 = 3
        self.RS  = 4
        self.E   = 5

        self.mega = avrBridgePy.avrBridge()
        self.init_lcd()
        self.lcd_clear()
        self.lcd_home()


    def command(self, list):
        for elem in list:
            self.mega.setPortPin(self.PORT, elem[0], elem[1])

    def enable(self):
        self.command(((self.E, 1),))
        #time.sleep(0.01)
        self.command(((self.E, 0),))

    def lcd_init4bit(self):
        self.command(((self.E, 0), (self.RS, 0)))
        self.command(((self.DB7, 0), (self.DB6, 0), (self.DB5, 1), (self.DB4, 1)))
        self.enable()
        self.enable()
        self.enable()
        self.command(((self.DB7, 0), (self.DB6, 0), (self.DB5, 1), (self.DB4, 0)))
        self.enable()
        #time.sleep(0.01*5)


    def lcd_data(self, byte):
        self.mega.setPortPin(self.PORT, self.RS, 1)
        self.mega.setPortPin(self.PORT, self.DB7, int(byte[0]))
        self.mega.setPortPin(self.PORT, self.DB6, int(byte[1]))
        self.mega.setPortPin(self.PORT, self.DB5, int(byte[2]))
        self.mega.setPortPin(self.PORT, self.DB4, int(byte[3]))
        self.enable()
        self.mega.setPortPin(self.PORT, self.DB7, int(byte[4]))
        self.mega.setPortPin(self.PORT, self.DB6, int(byte[5]))
        self.mega.setPortPin(self.PORT, self.DB5, int(byte[6]))
        self.mega.setPortPin(self.PORT, self.DB4, int(byte[7]))
        self.enable()
        #time.sleep(0.01*5)

    def lcd_command(self, byte):
        self.mega.setPortPin(self.PORT, self.RS, 0)
        self.mega.setPortPin(self.PORT, self.DB7, int(byte[0]))
        self.mega.setPortPin(self.PORT, self.DB6, int(byte[1]))
        self.mega.setPortPin(self.PORT, self.DB5, int(byte[2]))
        self.mega.setPortPin(self.PORT, self.DB4, int(byte[3]))
        self.enable()
        self.mega.setPortPin(self.PORT, self.DB7, int(byte[4]))
        self.mega.setPortPin(self.PORT, self.DB6, int(byte[5]))
        self.mega.setPortPin(self.PORT, self.DB5, int(byte[6]))
        self.mega.setPortPin(self.PORT, self.DB4, int(byte[7]))
        self.enable()

    def lcd_data_string(self, string):
        for elem in string:
            self.lcd_data(lcd.char2bin(elem))


    def lcd_clear(self):
        self.lcd_command("00000001")

    def lcd_home(self):
        self.lcd_command("00000010")


    #Entry mode: 0b000001is
    #Legt die Cursor Richtung sowie eine mögliche Verschiebung des Displays fest
    #i = 1, Cursorposition bei Ausgabe eines Zeichens erhöhen
    #i = 0, Cursorposition bei Ausgabe eines Zeichens vermindern
    #s = 1, Display wird gescrollt, wenn der Cursor das Ende/Anfang, je nach Einstellung von i, erreicht hat.
    def lcd_entrymode(self):
        #            000001is
        self.lcd_command("00000110")


    #On/off control: 0b00001dcb
    #Display insgesamt ein/ausschalten; den Cursor ein/ausschalten; den Cursor auf blinken schalten/blinken aus. Wenn das Display ausgeschaltet wird, geht der Inhalt des Displays nicht verloren. Der vorher angezeigte Text wird nach wiedereinschalten erneut angezeigt. Ist der Cursor eingeschaltet, aber Blinken ausgeschaltet, so wird der Cursor als Cursorzeile in Pixelzeile 8 dargestellt. Ist Blinken eingeschaltet, wird der Cursor als blinkendes ausgefülltes Rechteck dargestellt, welches abwechselnd mit dem Buchstaben an dieser Stelle angezeigt wird.
    #d = 0, Display aus
    #d = 1, Display ein
    #c = 0, Cursor aus
    #c = 1, Cursor ein
    #b = 0, Cursor blinken aus
    #b = 1, Cursor blinken ein
    def lcd_control(self):
        #            00001dcb
        self.lcd_command("00001100")


    #Cursor/Scrollen: 0b0001srxx
    #Bewegt den Cursor oder scrollt das Display um eine Position entweder nach rechts oder nach links.
    #s = 1, Display scrollen
    #s = 0, Cursor bewegen
    #r = 1, nach rechts
    #r = 0, nach links
    def lcd_curscr(self):
        #            0001srxx
        self.lcd_command("00001100")

    #Konfiguration: 0b001dnfxx
    #Einstellen der Interface Art, Modus, Font
    #d = 0, 4-Bit Interface
    #d = 1, 8-Bit Interface
    #n = 0, 1 zeilig
    #n = 1, 2 zeilig
    #f = 0, 5x7 Pixel (wird dont care wenn n=1)
    #f = 1, 5x11 Pixel
    def lcd_config(self):
        #            001dnfxx
        self.lcd_command("00101100")


    def init_lcd(self):
        self.lcd_init4bit()
        self.lcd_config()
        self.lcd_entrymode()
        self.lcd_control()


    def lcd_2nd_line(self, string):
        for i in range(0,40):
            #            0001srxx
            l.lcd_command("00010100")

        l.lcd_data_string(lcd.fillSpace(string))


    @staticmethod
    def fillZero(string, size):
        rest = size-string.__len__()
        for i in range(0, rest):
            string='0'+string
        return string

    @staticmethod
    def fillSpace(string, size):
        rest = size-string.__len__()
        for i in range(0, rest):
            string+=" "
        return string

    @staticmethod
    def char2bin(c):
        c = ord(c)
        i=c
        result = ""
        while not i == 0:
            result = str(i%2)+result
            i = i/2
        return lcd.fillZero(result, 8)


if __name__ == "__main__":

    l = lcd()

    for i in range(0,40):
        #            0001srxx
        l.lcd_command("00010100")

    l.lcd_data_string("Stop   Love   Ban   Skip")


    #        ("123456789 123456789 1234x6789 123456789 ")

    data = ("Caivorse Unite","by Blockhead")

    while True:
        for elem in data:
            l.lcd_home()
            l.lcd_data_string(lcd.fillSpace(elem, 24))
            time.sleep(5)


