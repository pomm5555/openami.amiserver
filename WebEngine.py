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

#    def index(self):
#
#        head = '''
#        '''
#
#        result = self.root.toHtml()
#        return "<html><head>"+head+"</head><body>"+result+"</body></html>"
#    index.exposed = True


    def index(self):

        head = '''
        <script type="text/javascript" src="http://www.google.com/jsapi"></script>
        <script type="text/javascript"> google.load("jquery", "1.3.2"); </script>
        <script src="servant@jabber.org/Filesystem/html/jqtouch/jqtouch.min.js" type="application/x-javascript" charset="utf-8"></script>
        <style type="text/css" media="screen">@import "servant@jabber.org/Filesystem/html/jqtouch/jqtouch.min.css";</style>
        <style type="text/css" media="screen">@import "servant@jabber.org/Filesystem/html/themes/apple/theme.min.css";</style>
        <script type="text/javascript" charset="utf-8">
        $(document).ready(function(){
            $.jQTouch({
                icon: 'jqtouch.png',
                statusBar: 'black-translucent',
                preloadImages: [
                    'themes/jqt/img/chevron_white.png',
                    'themes/jqt/img/bg_row_select.gif',
                    'themes/jqt/img/back_button_clicked.png',
                    'themes/jqt/img/button_clicked.png'
                    ]
            });
        });
        </script>

        '''

        result = self.root.toJqHtml()
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
    
    
    # This part of the program parses the URL which was called by a browser
    # and calls the use method... jqtouch style
#    def default(self, *args, **kwargs):
#
#	addr = ""
#	for elem in args:
#	    addr += "/"+elem
#
#        try:
#	    string = kwargs["string"]
#            result = self.root.getByAddress(addr[1:]).use(string)
#	except:
#            result = self.root.getByAddress(addr[1:]).use()
#            string = ""
#
#	try:
#            return '<html><head/><body><div id="get"><div class="toolbar"></div><div class="info">'+result+'</div></div></body></html>'
#	    #return "+ "+str(type(result))+kwargs.__str__()+" | "+string+"<br/>\n"+result
#	except:
#	    return "- "+str(type(result))+kwargs.__str__()+"<br/>\n"+string+"<br/>\n"#+result
#
#    default.exposed = True




    


if __name__ == "__main__":
    we = XMPPEngine("hallo")
