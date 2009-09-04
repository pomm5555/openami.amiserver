import os
from AmiTree import Container
from PlugIn import PlugIn
from Address import Address
from amiConfig import Config
from EventEngine import EventEngine

class Defaults(PlugIn):


    def __init__(self, token, configFile):

        #plugin itself
        self.content = Container("plugin", token, "This is a Defaults Plugin")

        # add container, set information to standard-path from config
        self.content.addContainer("cmd", "Play", Config.audioPlay, self.play)


	self.content.addContainer("cmd", "Stop", Config.audioStop, self.stop)

    def play(self, string="http://www.munich-radio.de:8000"):
        string = self.getText(string)
        address = Address(Config.audioStop)
    	EventEngine.root.getByAddress(address.__str__()).use(self, string)

    def stop(self, string=""):
        string = self.getText(string)
        address = Address(Config.audioStop)
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