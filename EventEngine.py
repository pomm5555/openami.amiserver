from CommunicationEngine import CommunicationEngine
from PlugIns import PlugIns
from amiConfig import Config
from AmiTree import Container
from WebEngine import WebEngine

class EventEngine:

    configFile = 'server.properties'
    root = Container("root", "root", "this is the root node")

    def __init__(self):

        webserver = WebEngine(EventEngine.root)

        #print "initializing EventEngine..."
        EventEngine.root.addContainer("instance", Config.jid, "this is the tree instance "+Config.jid)

        # assign me node to Eventengine.root.me
        EventEngine.root.me = EventEngine.root.getChild(Config.jid)

        # generate all plugins
        p = PlugIns(Config.plugInsFolder, EventEngine.configFile).getChildList()

        # load plugin tree into me-node
        EventEngine.root.me.addChildList(p)

        # assign address index cache to root.addressIndex
        self.updateAddressCache()

        #print EventEngine.root.returnTree(0)

        print "starting xmpp client..."

        com = CommunicationEngine(EventEngine.root)
        
        print "end"

    def loadPlugins(self):

        # - Load system plugin

        p = PlugIns(Config.plugInsFolder, configFile)
        plugins = p.getTree()

        print plugins.printTree(0)
        print "---------------------"
        print plugins.getAddressList()
        print "----------------------"


        print "Plugins loaded sucessfully."
        return plugins


    def updateAddressCache(self):
        EventEngine.root.me.addressIndex = EventEngine.root.me.getAddressList()


