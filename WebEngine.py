import cherrypy, time
from threading import Thread
from Address import Address
from amiConfig import Config

class WebEngine(Thread):

    def __init__(self, root):
        Thread.__init__(self)
	self.root = root
	#self.daemon = True
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

        addr = Config.get("server", "token")

        head = '''
        <script type="text/javascript" src="'''+addr+'''/Filesystem/html/jquery.js"></script>
        <script src="'''+addr+'''/Filesystem/html/jqtouch/jqtouch.min.js" type="application/x-javascript" charset="utf-8"></script>
        <style type="text/css" media="screen">@import "'''+addr+'''/Filesystem/html/jqtouch/jqtouch.min.css";</style>
        <style type="text/css" media="screen">@import "'''+addr+'''/Filesystem/html/themes/apple/theme.min.css";</style>
        <script type="text/javascript" charset="utf-8">
        $(document).ready(function(){
            $.jQTouch({
                icon: 'jqtouch.png',
                statusBar: 'black-translucent',
                preloadImages: [
                    ' '''+addr+'''/Filesystem/html/themes/jqt/img/back_button_clicked.png',
                    ' '''+addr+'''/Filesystem/html/themes/jqt/img/button_clicked.png'
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
            
	    string = kwargs["string"]
            print "with parameter: "+string
            result = self.root.getByAddress(addr[1:]).use(string)
            print "called use"
	except:
            print "call without parameter: "+addr[1:]
            result = self.root.getByAddress(addr[1:]).use()
            print "called without parameter"
            string = ""


	try:
            if not addr.find("Filesystem")  == -1:
                return result
            else:
                return '<div id="get"><div class="toolbar"><h1>Result</h1><a class="back" href="#">Back</a></div><div class="info">'+result+'</div></div>'
	except:
	    return '<div id="get"><div class="toolbar"><h1>Result</h1><a class="back" href="#">Back</a></div><div class="info">done</div></div>'
    default.exposed = True


    


if __name__ == "__main__":
    we = XMPPEngine("hallo")
