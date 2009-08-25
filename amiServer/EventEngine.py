# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "markus"
__date__ = "$Aug 13, 2009 11:02:27 PM$"


from CommunicationEngine import CommunicationEngine
from PlugIns import PlugIns
import os, ConfigParser



configFile = 'server.properties'

class EventEngine:

    def __init__(self):

        self.readConfig()
        self.root = self.loadPlugins()
        com = CommunicationEngine(self.root, self.jid, self.pwd, self.host, self.port, self.ressource)
        print "end"

    def readConfig(self):
        
        config = ConfigParser.ConfigParser()
        config.readfp(open(configFile))

        # parsing jabber section
        self.jid = config.get('jabber', 'jid')
        self.pwd = config.get('jabber', 'pwd')
        self.host = config.get('jabber', 'host')
        self.port = config.get('jabber', 'port')
        self.ressource = config.get('jabber', 'ressource')


        # parsing system section
        self.token = config.get('server', 'token')
        self.information = config.get('server', 'information')

        # parsing plugins section
        self.plugInsFolder = config.get('Plugins', 'PlugInsFolder')

        print "Read config successfuly."


    def loadPlugins(self):

        # - Load system plugin

        p = PlugIns(self.token, self.information, self.plugInsFolder, configFile)
        root = p.getTree()

        print root.printTree(0)
        

        print "Plugins loaded sucessfully."
        return root


if __name__ == "__main__":
    main()