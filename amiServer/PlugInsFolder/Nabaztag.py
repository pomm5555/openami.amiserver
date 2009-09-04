# To change this template, choose Tools | Templates
# and open the template in the editor.
# growlnotify -m "hallo" -t "hallo"


import os
from AmiTree import Container
from PlugIn import PlugIn

class Nabaztag(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"

        #plugin itself
        self.content = Container("plugin", token, "This is a Nabaztag Plugin")

        # set add container
        self.content.addContainer("cmd", "Play", "Play Stream on Nabaztag", self.play)

	self.content.addContainer("cmd", "Stop", "Stop Nabaztag", self.stop)

    def play(self, text="http://www.munich-radio.de:8000"):
        text = self.getText(text)
        print text
        os.system('curl http://api.nabaztag.com/vl/FR/api_stream.jsp?token=1230219014&sn=0019DB9C502A&urlList='+text)

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