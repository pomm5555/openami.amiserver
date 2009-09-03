import socket
import sys
import commands
import os
from subprocess import call,Popen,PIPE


def parseAddr(addr):
        global command
        global arg0
        global host
        global arg1

	command_arg = addr.split(" ")
	if len(command_arg) > 1:
            arg1 = command_arg[1]
	command_tree = command_arg[0].split("/")

        if len(command_tree) > 3:
            host = command_tree[1]
            command = command_tree[2]
            arg0 = command_tree[3]

	
# create socker
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ''
port = int(sys.argv[1])

command = ''
arg0 = ''
arg1 = ''

# bind port
s.bind((host, port))

#accept client 
while 1:
	s.listen(1)
	conn, addr = s.accept()
	print 'client addr: ', addr

	data = conn.recv(1000000)
	data =  data
	
	print 'client :' ,addr, 'sent', data
	if data == 'stream_on':
		ret = commands.getoutput('python ami_ee_client.py blahhtpc 555 stream_on')
		commands.getoutput('python ami_ee_client.py blahdesk 555 stream_on')
		conn.send(ret)
		conn.close()
	if data == 'stream_off':
		ret =commands.getoutput('python ami_ee_client.py blahdesk 555 stream_off')
		commands.getoutput('pyton ami_ee_client.py blahhtpc 555 stream_off') 
		conn.send(ret)
		conn.close()
	if data == 'volup':
		commands.getoutput('aumix -w +10')
		conn.close()
	if data == 'voldown':
		commands.getoutput('aumix -w -10')
		conn.close()	
	else:	
		parseAddr(data)
                print host + ":" + command + " " +  arg0 + " " + arg1
                cmd = command + " " +  arg0 + " " + arg1 + "&"
                commands.getoutput('pyton ami_ee_client.py ' + host + ' 555 ' + ' stream_off')
                conn.close()


