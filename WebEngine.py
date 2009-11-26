import cherrypy, time
from threading import Thread
from Address import Address
from amiConfig import Config
from AmiTree import *

class WebEngine(Thread):

    def __init__(self, root):
        Thread.__init__(self)
        self.root = root
        self.daemon = False
        self.start()

    def run(self):
        cherrypy.config.update({'server.socket_host': '0.0.0.0',
                                'server.socket_port': 8080, })
        cherrypy.quickstart(WebServer(self.root))

class WebServer():

    def __init__(self, root):
        self.root = root

    def index(self):

        

        addr = Config.get("server", "token")

        head = '''
        <script type="text/javascript" src="''' + addr + '''/Filesystem/html/jquery.js"></script>
        <script src="''' + addr + '''/Filesystem/html/jqtouch/jqtouch.min.js" type="application/x-javascript" charset="utf-8"></script>
        <style type="text/css" media="screen">@import "''' + addr + '''/Filesystem/html/jqtouch/jqtouch.min.css";</style>
        <style type="text/css" media="screen">@import "''' + addr + '''/Filesystem/html/themes/jqt/theme.css";</style>
        <script type="text/javascript" charset="utf-8">
        $(document).ready(function(){
            $.jQTouch({
                icon: 'jqtouch.png',
                statusBar: 'black-translucent',
                preloadImages: [
                    ' ''' + addr + '''/Filesystem/html/themes/jqt/img/back_button_clicked.png',
                    ' ''' + addr + '''/Filesystem/html/themes/jqt/img/button_clicked.png'
                    ]
            });
        });
        </script>

        '''

        result = self.root.toJqHtml()
        return "<html><head>" + head + "</head><body>" + result + "</body></html>"
    index.exposed = True



    # This part of the program parses the URL which was called by a browser
    # and calls the use method...
    def default(self, *args, **kwargs):
        
        #print "BEGIN"
        #print args
        #print kwargs
        #print "END"
        
        str=""
        for elem in args:
            str+=elem+"/"
        for k, v in kwargs.items():
            str+=" "+k+"="+v    
        
        #return str
        
        # build url start
        addr = ""
        for elem in args:
            addr += "/" + elem
        addr= addr[1:]
    
        # get target object
        target = self.root.getByAddress(addr)

        try:
            string = kwargs["string"]
            print "with parameter: " + string
            result = target.use(string)
            print "called use"
        except:
            print "call without parameter: " + addr
            result = target.use()
            print "called without parameter"
            string = ""

        try:
            if "Filesystem" in addr:
                return result
            elif target.rendering == 0:
                return result
            elif target.rendering == 1:
                return '<div id="get"><div class="toolbar"><h1>Result</h1><a class="back" href="#">Back</a></div><div class="info">' + result + '</div></div>'
            else:
                return 'No Rendering No Service!'
            
        except:
            return '<div id="get"><div class="toolbar"><h1>Result</h1><a class="back" href="#">Back</a></div><div class="info">Exception??</div></div>'
            
            
    default.exposed = True


    


if __name__ == "__main__":
    we = XMPPEngine("hallo")
