import os
from AmiTree import Container
from PlugIn import PlugIn
from Address import Address
from amiConfig import Config
from EventEngine import EventEngine

class Defaults(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"


        #plugin itself
        self.content = Container("plugin", token, "This is a Defaults Plugin")

        for pair in Config.getSection("Defaults"):
            self.content.addContainer("cmd", pair[0], pair[1], self.general)

    def general(self, string=""):
        string = self.getText(string)
        address = Address(self.information)
    	EventEngine.root.getByAddress(address.__str__()).use(string)

    # returns the plugin as a tree
    def getTree(self):
        return self.content

    # just a little helper function
    def getText(self, var):
        try:
            var = var.strings["text"]
            return test
        except:
            return var