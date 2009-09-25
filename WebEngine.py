import cherrypy, time
from threading import Thread
from Address import Address

class WebEngine(Thread):

    def __init__(self, root):
        Thread.__init__(self)
	self.root = root
	#self.setDaemon(True)
	self.start()
	#while 1:
	#    print "running Webengine"
	#    time.sleep(5)

    def run(self):
        cherrypy.config.update({'server.socket_host': '0.0.0.0',
                                'server.socket_port': 8080,})
        cherrypy.quickstart(WebServer(self.root))

class WebServer():

    def __init__(self, root):
        self.root = root

    def index(self):

        head = ''' <link rel="stylesheet" type="text/css" href="classic.css" /> '''
        
        result = self.root.toHtml()
	#result = "hallo :D"
        return "<html><head></head><body>"+result+"</body></html>"
    index.exposed = True


    def default(self, *args, **kwargs):
        
	addr = ""
	for elem in args:
	    addr += "/"+elem

        
        try:
	    string = kwargs["string"]
	except:
	    string = ""


        result = self.root.getByAddress(addr[1:]).use(string)
        
	try:
	    return "+ "+str(type(result))+kwargs.__str__()+" | "+string+"<br/>\n"+result
	except:
	    return "- "+str(type(result))+kwargs.__str__()+"<br/>\n"+string+"<br/>\n"#+result
	
    default.exposed = True



if __name__ == "__main__":
    we = WebEngine("hallo")
