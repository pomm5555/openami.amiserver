# To change this template, choose Tools | Templates
# and open the template in the editor.
# growlnotify -m "hallo" -t "hallo"


import os
from AmiTree import Container
from PlugIn import PlugIn

class Madplay(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "openwrt"

        #plugin itself
        self.content = Container("plugin", token, "This is a Madplay Plugin")
        
        # set add container
        self.content.addContainer("cmd", "Play", "Play Madplay", self.play)

	self.content.addContainer("cmd", "Stop", "Stop Madplay", self.stop)

    def play(self, text="http://www.munich-radio.de:8000"):
        text = self.getText(text) 
        print text
        os.system('curl "'+text+'" | madplay - &' )

    def stop(self, string=""):
    	os.system('killall madplay')

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