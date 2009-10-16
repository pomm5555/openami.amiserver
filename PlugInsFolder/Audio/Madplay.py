# To change this template, choose Tools | Templates
# and open the template in the editor.
# growlnotify -m "hallo" -t "hallo"


import os, re
from AmiTree import Container
from PlugIn import PlugIn

class Madplay(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"

        #plugin itself
        self.content = Container("plugin", token, "This is a Madplay Plugin")

        #Plugin visibility, can be accessed, but is not listed
        self.visible = False
        
        # set add container
        self.content.addContainer("cmd", "Play", "Play Madplay", self.play)

	self.content.addContainer("cmd", "Stop", "Stop Madplay", self.stop)

    def play(self, text="http://www.munich-radio.de:8000"):
        print "trying to play: >"+str(text)+"<"
        text = self.getText(text)
        print "trying to play:"+text
        if re.match(".*?\.mp3", text):
            os.system("madplay \""+text+"\"")
            return "Playing File: "+text
        else:
            os.system('curl "'+text+'" | madplay - &' )
            return "Playing Stream: "+text

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

