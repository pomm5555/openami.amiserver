from xmppEngine import *
from PlugIns import PlugIns
from amiConfig import Config
from AmiTree import Container
from WebEngine import *

class EventEngine:


    def __init__(self, absPath):

        #Config.absPath = absPath
        #print ">"+absPath+"<"
        #print ">"+Config.absPath+"<"

        EventEngine.configFile = 'server.properties'
        EventEngine.root = Container("root", "root", "this is the root node")



        #print "initializing EventEngine..."
        EventEngine.root.addContainer("instance", Config.jid, "this is the tree instance "+Config.jid)

        # assign me node to Eventengine.root.me
        EventEngine.root.me = EventEngine.root.getChild(Config.jid)

        # generate all plugins
        p = PlugIns(Config.plugInsFolder, EventEngine.configFile).getChildList()

        # load plugin tree into me-node
        EventEngine.root.me.addChildList(p)

        # starting xmppEngine
        if Config.get("server", "jabber").__eq__("on"):
            print "starting xmppEngine"
            xmpp = XMPPEngineStart(EventEngine.root)
        else:
            print "jabber not active"

        # start webEngine
        if Config.get("server", "web").__eq__("on"):
            print "starting webEngine"
            webserver = WebEngine(EventEngine.root)

        print EventEngine.root.printTree(0)


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


