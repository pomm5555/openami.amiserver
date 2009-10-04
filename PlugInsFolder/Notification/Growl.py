# To change this template, choose Tools | Templates
# and open the template in the editor.
# growlnotify -m "hallo" -t "hallo"


import os
from AmiTree import Container
from PlugIn import PlugIn

class Growl(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "macos"

        #plugin itself
        self.content = Container("plugin", token, "this is a growl plugin")
        self.content.logging = True

        # set add container
        self.content.addContainer("cmd","Growl", "send growl notification", self.growl, logging=True)

    def growl(self, text="Notification"):
        text = self.getText(text)
        print text
        os.system('growlnotify -m "'+text+'" -t "Ami Notification"' )


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