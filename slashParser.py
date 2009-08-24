
def parseAddr(addr):
	command_arg = addr.split(" ")
	arg1 = command_arg[1]
	command_tree = command_arg[0].split("/")
	
	host = command_tree[1]
	command = command_tree[2]
	arg0 = command_tree[3]

	print host + ":" + command + " " +  arg0 + " " + arg1 
