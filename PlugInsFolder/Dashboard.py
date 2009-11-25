
from AmiTree import Container
from PlugIn import PlugIn
from xmppEngine import XMPPEngine
import Address

class Dashboard(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"


        #plugin itself
        self.content = Container("plugin", token, "This is a Status Plugin", self.getParts)
        self.content.rendering = Container.PLAIN
       

    def getParts(self, text=""):
        string = ""
        
        #addr = Address("/Services/JqHtml")
        #result = EventEngine.root.getByAddress(addr.__str__()).use()

        #res = self.root().__str__()
        
        javascript = '$.getJSON(\'/servant@jabber.org/System/Temperature/LivingRoom\', function(data){alert(\'Data Loaded: \' + data[0]);});'
        
        
        
        liElements = []
        
        liElements.append('<small>small</small>Big Text<em>Emphasized</em>')
        liElements.append('<small>small</small>Big Text<em>Emphasized</em>')
        liElements.append('<small>small</small>Big Text<em>Emphasized</em>')
        liElements.append('<small>small</small>Big Text<em>Emphasized</em>')
        
        list = ""
        for elem in liElements:
            list += '<li><a href="#">'+elem+'</a></li>'
        list = '<ul class="metal">'+list+'</ul>'
        
        result = '<div id="get"><div class="toolbar"><h1>Result</h1><a class="back" href="#">Back</a></div>'+list+'</div>'
        
        jscriptHook = '<img style="display:none;" src="/servant@jabber.org/Filesystem/interfaces/images/tabs_playlist.png" onload="'+javascript+'"/>'

        
        return result+jscriptHook
