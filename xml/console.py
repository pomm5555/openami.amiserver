import time
from xml.dom.minidom import parseString

energy_file = open("/home/jens/workspace/ami/src/xml/Energy.xml")
energyString =  energy_file.read()
energy_file.close()
energy_object = parseString(energyString)

eLevel = energy_object.getElementsByTagName('level0')
if str(eLevel) != '[]':
    eRoom = eLevel[0].getElementsByTagName('room0')
    if str(eRoom) != '[]':
        eDevice = eRoom[0].getElementsByTagName('device1')
        if str(eDevice) != '[]':
            eMonth = eDevice[0].firstChild.firstChild.data
            print eMonth
