# To change this template, choose Tools | Templates
# and open the template in the editor.
# growlnotify -m "hallo" -t "hallo"


import os
from AmiTree import Container
from PlugIn import PlugIn
from amiConfig import Config
from ctypes import cdll, c_int

class avrBridge(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"

        lib=Config.absPath+Config.avrLib
        print lib
        self.mega=cdll.LoadLibrary(lib)


        self.mega.initUsbLib()


        #plugin itself
        self.content = Container("plugin", token, "This is a avrBridge Plugin")
        self.content.visible = False


        # hide Plugin from showing up in xml, search, show...
        self.content.visible = False

        # set add container
        self.content.addContainer("cmd", "adc0", "get Adc 0 Value", self.adc0)


    def adc0(self, text=""):
        text = self.getText(text)
        print str(self.mega.getAdcPortPin(port,pin))

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