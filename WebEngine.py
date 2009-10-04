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

        head = ''''''
        #<script type="text/javascript" src="http://www.google.com/jsapi"></script>
        #<script type="text/javascript"> google.load("jquery", "1.3.2"); </script>
        #<script src="jqtouch/jqtouch.min.js" type="application/x-javascript" charset="utf-8"></script>
        #<style type="text/css" media="screen">@import "jqtouch/jqtouch.min.css";</style>
        #<style type="text/css" media="screen">@import "themes/jqt/theme.min.css";</style>
        #'''
        
        result = self.root.toHtml()
	#result = "hallo :D"
        return "<html><head>"+head+"</head><body>"+result+"</body></html>"
    index.exposed = True



    # This part of the program parses the URL which was called by a browser
    # and calls the use method...
    def default(self, *args, **kwargs):
        
	addr = ""
	for elem in args:
	    addr += "/"+elem

        
        try:
            print "with parameter"
	    string = kwargs["string"]
            print "parsed kwargs"
            result = self.root.getByAddress(addr[1:]).use(string)
            print "called use"
	except:
            print "call without parameter"
            result = self.root.getByAddress(addr[1:]).use()
            print "called without parameter"
            string = ""


        
        
	try:
            return result
	    #return "+ "+str(type(result))+kwargs.__str__()+" | "+string+"<br/>\n"+result
	except:
	    return "- "+str(type(result))+kwargs.__str__()+"<br/>\n"+string+"<br/>\n"#+result
	
    default.exposed = True



if __name__ == "__main__":
    we = XMPPEngine("hallo")
