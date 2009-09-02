
from AmiTree import Container
from PlugIn import PlugIn
from CommunicationEngine import CommunicationEngine

class Status(PlugIn):


    def __init__(self, token, configFile):

        #plugin itself
        self.content = Container("plugin", token, "This is a Status Plugin")

        # set add container
        self.content.addContainer("cmd", "Buddies", "Show Buddies", self.getBuddies)


    def getBuddies(self, text=""):
        string = ""

        for elem in CommunicationEngine.roster.getItems():
            string += elem+"\n"

        return string



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