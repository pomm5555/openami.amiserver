# To change this template, choose Tools | Templates
# and open the template in the editor.
# growlnotify -m "hallo" -t "hallo"


import os
from AmiTree import Container
from PlugIn import PlugIn

class Mpg123(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"


        #plugin itself
        self.content = Container("plugin", token, "This is a Mpg123 Plugin")

        # set add container
        self.content.addContainer("cmd", "Play", "Play Mpg123", self.play)

	self.content.addContainer("cmd", "Stop", "Stop Mpg123", self.stop)

    def play(self, text="http://www.munich-radio.de:8000"):
        text = self.getText(text)
        print text
        os.system('mpg123 '+text+' &' )

    def stop(self, string=""):
    	os.system('killall mpg123')

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