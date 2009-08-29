from CommunicationEngine import CommunicationEngine
from PlugIns import PlugIns
from amiConfig import Config
import os, ConfigParser




configFile = 'server.properties'

class EventEngine:

    def __init__(self):

        self.root = self.loadPlugins()
        self.root.addressIndex = self.root.getAddressList()
        com = CommunicationEngine(self.root)
        print "end"

    def loadPlugins(self):

        # - Load system plugin

        p = PlugIns(Config.token, Config.information, Config.plugInsFolder, configFile)
        root = p.getTree()

        print root.printTree(0)
        print "---------------------"
        print root.getAddressList()
        print "----------------------"


        print "Plugins loaded sucessfully."
        return root