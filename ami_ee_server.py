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
	
        parseAddr(data)
        print host + ":" + command + " " +  arg0 + " " + arg1
        cmd = command + " " +  arg0 + " " + arg1 + "&"

        conn.close()
        p1 = os.popen2(cmd)
        #sys.exit(0)

        conn.close()

