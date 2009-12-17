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

        #Muss vom Plugin generiert werden, damit es zu jeder zeit neu dynamisch geladen werden kann!
        navigationbar = '''
        <div class="floaty" style="display: block;">
            <ul>
                <li><a href='/'''+addr+'''/Dashboard' class="slideup">Dashboard</a></li>
                <li><a href='#'''+addr.replace('@', '_').replace('.', '_')+''''>Tree</a></li>
                <li><a href='/'''+addr+'''/System/FritzMonitor' class="flip">Kernel Info</a></li>
                <li><a href='/'''+addr+'''/Filesystem/interfaces/Player.interface' class="flip">Audioplayer</a></li>
            </ul>
        </div>
        '''

        addr = Config.get("server", "token")

        head = '''
        <meta charset="UTF-8" />

        <style type="text/css" media="screen">@import "'''+addr+'''/Filesystem/html/jqtouch/jqtouch.css";</style>
        <style type="text/css" media="screen">@import "'''+addr+'''/Filesystem/html/themes/jqt/theme.css";</style>
        <style type="text/css" media="screen">@import "'''+addr+'''/Filesystem/html/ami.css";</style>
        <script src="'''+addr+'''/Filesystem/html/jqtouch/jquery.1.3.2.min.js" type="text/javascript" charset="utf-8"></script>
        <script src="'''+addr+'''/Filesystem/html/jqtouch/jqtouch.js" type="application/x-javascript" charset="utf-8"></script>
        <!--<script src="'''+addr+'''/Filesystem/html/extensions/jqt.offline.js" type="application/x-javascript" charset="utf-8"></script>-->
        <script src="'''+addr+'''/Filesystem/html/extensions/jqt.floaty.js" type="application/x-javascript" charset="utf-8"></script>
        <script type="text/javascript" charset="utf-8">
            var jQT = new $.jQTouch({
                icon: '/'''+addr+'''/Filesystem/html/images/appIcon.png',
                addGlossToIcon: true,
                cacheGetRequests: false,
                startupScreen: '/'''+addr+'''/Filesystem/html/images/startup.png',
                statusBar: 'black'
            });


            $(function(){

                $('.togglefloaty').click(function(){
                    $('.floaty').toggleFloaty();
                    $(this).removeClass('active');
                    return false;
                });

                $('.floaty').makeFloaty({
                    spacing: 380,
                    time: '0.0s'
                });

            });
            
        </script>
        '''

        result = self.root.toJqHtml()
        return '<html ><head>' + head + '</head><body>' + result + navigationbar + '</body></html>'
        # manifest="/'+addr+'/Filesystem/html/cache.manifest"
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
                return '<div id="'+addr+'"><div class="toolbar"><h1>Result</h1><a class="back" href="#">Back</a></div><div class="info">' + result + '</div></div>'
            else:
                return 'No Rendering No Service!'
            
        except:
            return '<div id="'+addr+'"><div class="toolbar"><h1>Result</h1><a class="back" href="#">Back</a></div><div class="info">Exception??</div></div>'
            
            
    default.exposed = True