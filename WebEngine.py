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
                                'server.socket_port': 8080})
                                

        cherrypy.quickstart(WebServer(self.root))

class WebServer():

    _cp_config = {'tools.gzip.on': True}

    def __init__(self, root):
        self.root = root
        
    def index(self):
        self.contentType('text/html')

        addr = Config.get("server", "token")

        #Muss vom Plugin generiert werden, damit es zu jeder zeit neu dynamisch geladen werden kann!
        navigationbar = '''
        <div class='floaty'>
            <ul>
                <li><a href='/'''+addr+'''/Dashboard' class="slideup">Dashboard</a></li>
                <li><a href='#'''+addr.replace('@', '_').replace('.', '_')+'''' class="">Home</a></li>
                <li><a href='/'''+addr+'''/Filesystem/interfaces/Map.interface' class="">Map</a></li>
                <li><a href='/'''+addr+'''/Filesystem/interfaces/Player.interface' class="">Audio</a></li>
            </ul>
        </div>
        '''

        addr = Config.get("server", "token")

        head = '''
        <meta charset="UTF-8" />

        <style type="text/css" media="screen">@import "'''+addr+'''/Filesystem/html/jqtouch/jqtouch.css";</style>
        <style type="text/css" media="screen">@import "'''+addr+'''/Filesystem/html/themes/jqt/theme.css";</style>
        <style type="text/css" media="screen">@import "'''+addr+'''/Filesystem/html/ami.css";</style>
        <style type="text/css" media="screen">@import "'''+addr+'''/Filesystem/interfaces/css/player.css";</style>
        <script src="'''+addr+'''/Filesystem/html/jqtouch/jquery.1.3.2.min.js" type="text/javascript" charset="utf-8"></script>
        <!--script src="'''+addr+'''/Filesystem/html/jqtouch/jqtouch.transitions.js" type="text/javascript" charset="utf-8"></script-->
        <script src="'''+addr+'''/Filesystem/html/jqtouch/jqtouch.js" type="application/x-javascript" charset="utf-8"></script>
        <!--script src="'''+addr+'''/Filesystem/html/extensions/jqt.offline.js" type="application/x-javascript" charset="utf-8"></script-->
        <script src="'''+addr+'''/Filesystem/html/extensions/jqt.floaty.js" type="application/x-javascript" charset="utf-8"></script>
        <script type="text/javascript" charset="utf-8">
            var jQT = new $.jQTouch({
                icon: '/'''+addr+'''/Filesystem/html/images/appIcon.png',
                addGlossToIcon: true,
                cacheGetRequests: false,
                startupScreen: '/'''+addr+'''/Filesystem/html/images/startup.png',
                statusBar: 'black-translucent'
            });


            $(function(){

                $('.togglefloaty').click(function(){
                    $('.floaty').toggleFloaty();
                    $(this).removeClass('active');
                    return false;
                });


                $('.floaty').makeFloaty({
                    spacing: 0,
                    time: '0.2s',
                    align: 'bottom'
                });

                $('.arrow').bind("swipe",function(event, data){
                    if(data.direction=='right') {
                        if (true){
                            alert($(this).children(".removebutton").html())
                            $(this).append("<small class='counter removebutton' onClick='$(this).parent().hide();'>remove</small>");
                        } else {
                            alert('there is already a button')
                        }
                    }else {
                        print
                        $('.removebutton').hide();
                    }
                });                

            });
            
        </script>
        '''

        result = self.root.toJqHtml()
        
        # control caching
        caching = False
        if caching:
            manifest=' manifest="/cache.manifest"'
        else:
            manifest=''
        return '<html'+manifest+'><head>' + head + '</head><body>' + result + navigationbar + '</body></html>'
    index.exposed = True

    # This part of the program parses the URL which was called by a browser
    # and calls the use method..
    
    def default(self, *args, **kwargs):

        jid = Config.get("server", "token")

        self.contentType('text/html')
        
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

        #print '* '+addr
        addr= addr[1:]

        if Config.get("server", "caching") == 'on':
            cachrev = Config.get("server", "interfacerev")
        else:
            cachrev = time.time().__str__()



        if addr.__eq__('cache.manifest'):
            #print 'CACHE MANIFEST REQUEST!!!!!'
            self.contentType('text/cache-manifest')
            return '''CACHE MANIFEST
#revision '''+cachrev+'''
'''+jid+'''/Filesystem/html/themes/jqt/theme.css
'''+jid+'''/Filesystem/html/ami.css
'''+jid+'''/Filesystem/html/jqtouch/jquery.1.3.2.min.js
'''+jid+'''/Filesystem/html/jqtouch/jqtouch.css
'''+jid+'''/Filesystem/html/extensions/jqt.floaty.js
'''+jid+'''/Filesystem/html/jqtouch/jqtouch.js
'''+jid+'''/Filesystem/html/themes/jqt/img/toolbar.png
'''+jid+'''/Filesystem/html/themes/jqt/img/button.png
'''+jid+'''/Filesystem/html/themes/jqt/img/back_button.png
'''+jid+'''/Filesystem/html/themes/jqt/img/chevron.png
'''+jid+'''/Filesystem/html/themes/jqt/img/on_off.png
'''+jid+'''/Filesystem/html/themes/jqt/img/loading.gif
'''+jid+'''/Filesystem/html/images/appIcon.png
'''+jid+'''/Filesystem/html/images/startup.png
'''+jid+'''/Filesystem/interfaces/images/bg_bottom.png
'''+jid+'''/Filesystem/interfaces/images/bg_title.png
'''+jid+'''/Filesystem/interfaces/images/control_backward.png
'''+jid+'''/Filesystem/interfaces/images/control_ban.png
'''+jid+'''/Filesystem/interfaces/images/control_forward.png
'''+jid+'''/Filesystem/interfaces/images/control_love.png
'''+jid+'''/Filesystem/interfaces/images/control_play.png
'''+jid+'''/Filesystem/interfaces/images/control_stop.png
'''+jid+'''/Filesystem/interfaces/images/map.png
'''+jid+'''/Filesystem/interfaces/images/tabs_audiosink.png
'''+jid+'''/Filesystem/interfaces/images/tabs_magnifier.png
'''+jid+'''/Filesystem/interfaces/images/tabs_playlist.png
'''+jid+'''/Filesystem/interfaces/images/tabs_controls.png
'''+jid+'''/Filesystem/interfaces/images/test.png
'''+jid+'''/Filesystem/interfaces/css/player.css




NETWORK:
/'''+jid+'''/
'''

        if addr.__eq__('favicon.ico'):
            addr = Address('/Filesystem/html/images/favicon.ico')
            return self.root.getByAddress(addr).use()


        self._cp_config = {'response.headers.Content-Type': 'text/html'}
        # get target object
        target = self.root.getByAddress(addr)


        try:
            string = kwargs["string"]
            #print "with parameter: " + string
            result = target.use(string)
            #print "called use"
        except:
            print "\** called: " + addr
            
            result = target.use()
            #print "called without parameter"
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


    def contentType(self, type):
        cherrypy.response.headers['Content-Type'] = type
        #print cherrypy.response.headers['Content-Type']
        
