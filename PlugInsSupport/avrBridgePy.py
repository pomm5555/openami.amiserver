from ctypes import c_int
from ctypes import cdll
import time


class avrBridge():
    '''
        avrBridge is a avrBridgeC Library Binding.
        GPIO:
                PB0, PB4-PB5
                PC0-PC4
                PD0-PD1, PD3, PD5-7 (Using PD2 or PD4 is not possible because
                            the USB is connected to it.

        DAC:
                PB1-PB3

        ADC:
                PC0-PC5
    '''

    PORTB = 0
    PORTC = 1
    PORTD = 2

    DAC0 = 0
    DAC1 = 2
    DAC2 = 3

    ADC0 = 0
    ADC1 = 1
    ADC2 = 2
    ADC3 = 3
    ADC4 = 4
    ADC5 = 5
    ADC6 = 6
    ADC7 = 7

    OUT = 1
    IN = 0

    ON = 1
    OFF = 0

    def __init__(self):
        lib = "../PlugInsSupport/libavrBridgeC.dylib"
        self.mega = cdll.LoadLibrary(lib)
        self.mega.initUsbLib()

    def setDac(self, PIN, VALUE):
        ''' PIN is in range(0,2),
            avrBridge Ports are PB1-PB3
            TODO sets Pins as output everytime, could be optized'''

        self.mega.setPortPinDir(avrBridge.PORTB, PIN + 1, avrBridge.OUT)
        self.mega.setDac(PIN, VALUE)

    def setPortPin(self, PORT, PIN, ON):
        #self.mega.setPortPinDir(PORT, PIN, 1)
        self.mega.setPortPin(PORT, PIN, ON)

    def getPortPin(self, PORT, PIN):
        self.mega.setPortPinDir(PORT, PIN, avrBridge.IN) #DIRECTION
        self.mega.setPortPin(PORT,PIN,avrBridge.ON) #PULLDOWN
        return self.mega.getPortPin(PORT,PIN)

    def getAdc(self, PIN, PORT=2):
        self.mega.setPortPinDir(PORT, PIN, 0) #INPUT
        self.mega.setPortPin(PORT, PIN, 1) #PULLDOWN
        return self.mega.getAdcPortPin(PORT, PIN) # READ



if __name__ == "__main__":


    mega = avrBridge()

    # DAC TEST
#    VALUE=2
#    while True:
#        if VALUE >=255:
#            VALUE=2
#        else:
#            VALUE += VALUE/2
#
#        for PIN in (0,1,2):
#            mega.setDac(PIN, VALUE)
#            print str(PIN) + '-' + str(VALUE)


    # GPIO OUTPUT TEST
#    while True:
#        PORT = 2
#        ON = int(time.time() % 2)
#        print ON
#        for PIN in (0, 1, 3):
#            mega.setPortPin(PORT, PIN, ON)
#        time.sleep(1)

    # GPIO Input TEST
#    cache = 1
#    while True:
#        value = (mega.getPortPin(1,0)+1)%2
#        if not cache == value:
#            cache = value
#            print value


    # ADC TEST
    # Ive tested with a potentiometer,
    # connected it to ADC and GND
#    PIN = 5
#
#    cache = 0
#    while True:
#        val = int(((mega.getAdc(PIN)-28)/742.)*100)
#        #print val
#        if abs(cache-val)>2:
#            cache = val
#            print val









