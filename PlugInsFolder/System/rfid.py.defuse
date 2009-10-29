import os
from AmiTree import Container
from PlugIn import PlugIn

##
# OSX and AppleScript specific plugin that controls some Finder/System functionality
##
class rfid(PlugIn):
	
    def __init__(self, token, configFile):

        #plugin itself
        self.content = Container("plugin", token, "This is a rfid Plugin")

        # set add container

        self.content.addContainer("cmd","last", "get last seen tag", self.getLast)


    def getTree(self):
        return self.content

    def getLast(self, string=""):
    	#lastTag = os.system("python /Users/ka010/share/workspace/python/ami_ce-tmp/amiServer/PlugInsSupport/rfid/rfidLastTag")
    	f = open('/Users/ka010/share/workspace/python/ami_ce-tmp/amiServer/PlugInsSupport/rfid/rfidLastTag', 'r')
    	lastTag = f.read()    	
        return lastTag

    """
    Packet to test say:
    <?xml version="1.0" ?>
    <packet from="fernmelder@jabber.org" to="/Finder/Say">
        <string name="text">
            Hello master, my name is hal2000
        </string>
    </packet>
    """

    def getText(self, var):
        try:
            var = var.strings["text"]
            return test
        except:
            return var