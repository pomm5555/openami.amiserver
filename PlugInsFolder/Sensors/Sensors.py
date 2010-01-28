import os
from AmiTree import Container
from PlugIn import PlugIn
from Address import Address
from amiConfig import Config
from EventEngine import EventEngine

class Sensors(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"
        self.jid = Config.get("jabber","jid")
        #plugin itself
        self.content = Container("plugin", token, "This is a Sensors Plugin")
	cmd=""
        for pair in Config.getSection("Sensors"):
            if '?' in pair[1]:
            	tmp = pair[1].split('?')
            	self.content.arg = tmp[1].replace('string=','')
		cmd = tmp[0]
            else:
            	self.content.arg=""
            
            if pair[0].endswith('_plain'):
                title= pair[0].replace('_plain','')
                container = Container("cmd",title,pair[1],self.general)
                container.rendering = Container.PLAIN
            else:
                container = Container("cmd",pair[0],cmd,self.general)
            self.content.addChild(container)
            
            #self.content.addContainer("cmd", pair[0], pair[1], use=self.general, args="test")
            
        
    def general(self, string=None):
        address = Address(self.information)

        if not self.getParent().arg:
	    print '\n *** sensors - NO-USE- trying to use: ', address , " with: " , self.getParent().arg 
            return EventEngine.root.getByAddress(address.__str__()).use()
        print '\n *** sensors - USE -  trying to use: ', address  , 'with : ' , self.getParent().arg 
        string = self.getText(string)
    	return EventEngine.root.getByAddress(address.__str__()).use(self.getParent().arg)

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