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

        navigationbar = '''
        <span id='navigationbar'>
            <ul>
                <li><a href='geheim@jabber.org/Dashboard'>Dashboard</a></li>
                <li><a href='#geheim_jabber_org'>Tree</a></li>
                <li><a href='#geheim_jabber_org'>Ami Info</a></li>
                <li><a href='#geheim_jabber_org'>Network Info</a></li>
            </ul>
        </span>
        '''

        addr = Config.get("server", "token")

        head = '''
        <meta charset="UTF-8" />

        <style type="text/css" media="screen">@import "'''+addr+'''/Filesystem/html/jqtouch/jqtouch.css";</style>
        <style type="text/css" media="screen">@import "'''+addr+'''/Filesystem/html/themes/jqt/theme.css";</style>
        <style type="text/css" media="screen">@import "'''+addr+'''/Filesystem/html/ami.css";</style>
        <script src="'''+addr+'''/Filesystem/html/jqtouch/jquery.1.3.2.min.js" type="text/javascript" charset="utf-8"></script>
        <script src="'''+addr+'''/Filesystem/html/jqtouch/jqtouch.js" type="application/x-javascript" charset="utf-8"></script>
        <script src="'''+addr+'''/Filesystem/html/extensions/jqt.offline.js" type="application/x-javascript" charset="utf-8"></script>
        <script type="text/javascript" charset="utf-8">
            var jQT = new $.jQTouch({
                icon: ' '''+addr+'''/Filesystem/html/images/appIcon.png',
                addGlossToIcon: true,
                startupScreen: ' '''+addr+'''/Filesystem/html/images/startup.png',
                statusBar: 'black'
            });

            $(function(){
                // Custom Javascript (onReady)
            });
        </script>
        <style type="text/css" media="screen">
            /* Custom Style */
        </style>
        '''

        result = self.root.toJqHtml()
        return '<html manifest="/'+addr+'/Filesystem/html/cache.manifest"><head>' + head + '</head><body>' + result + navigationbar + '</body></html>'
    index.exposed = True



    # This part of the program parses the URL which was called by a browser
    # and calls the use method...
    def default(self, *args, **kwargs):
        
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