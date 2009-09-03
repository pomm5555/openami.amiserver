import serial
import os

while 1:
	ser = serial.Serial('/dev/tty.PL2303-0000101D', 9600, timeout=1)

	s = ser.read(10)        # read up to ten bytes (timeout)
	#line = ser.readline()   # read a '\n' terminated line
	print s
	if (s != ""):
		os.system('echo  '+ s +' > /Users/ka010/share/workspace/python/ami_ce-tmp/amiServer/PlugInsSupport/rfid/rfidLastTag')
	
	ser.close()
