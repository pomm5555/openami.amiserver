from CommunicationEngine import CommunicationEngine
from PlugIns import PlugIns
from amiConfig import Config
from AmiTree import Container



class EventEngine:

    configFile = 'server.properties'
    root = Container("root", "root", "this is the root node")

    def __init__(self):

        EventEngine.root.addContainer("instance", Config.jid, "this is the tree instance "+Config.jid)

        # assign me node to Eventengine.root.me
        EventEngine.root.me = EventEngine.root.getChild(Config.jid)

        # generate all plugins
        p = PlugIns(Config.plugInsFolder, EventEngine.configFile).getTree()
        #print p.content


        # load plugin tree into me-node
        EventEngine.root.me.content.update(p.content)


        # assign address index cache to root.addressIndex
        EventEngine.root.me.addressIndex = EventEngine.root.me.getAddressList()

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