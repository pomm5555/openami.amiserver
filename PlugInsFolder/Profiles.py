# To change this template, choose Tools | Templates
# and open the template in the editor.
# growlnotify -m "hallo" -t "hallo"


import os
from AmiTree import Container
from PlugIn import PlugIn
from Address import Address
from ConfigParser import ConfigParser
from amiConfig import Config

class Profiles(PlugIn):

    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"
        
        config = ConfigParser()
        configpath = Config.absPath+'/properties/profiles.properties'
        config.readfp(open(configpath))
        

        #plugin itself
        self.content = Container("plugin", token, "This Plugin activates predefined amiServer States, known as Profiles.", self.rootdo)

	for profile in config.sections():
            batch = []
            for tuple in config.items(profile):
                batch.append(tuple[1])
            self.content.addContainer("cmd", profile, batch, self.batch)

    def rootdo(self, text=""):
        return "There are no Profiles loaded"


    def batch(self, text=""):
        print 'executing profile'
        for address in self.information:
            addr = Address(address)
            print addr.__str__()
            self.root().getByAddress(addr.__str__()).use()

        print 'profile acrivated'
        return "should have been generated automatically"+self.token
