
from AmiTree import Container
from PlugIn import PlugIn
from xmppEngine import XMPPEngine
from amiConfig import Config
import os
import re

class Global(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"


        #plugin itself
        self.content = Container("plugin", token, "This is a global Status Plugin")
        self.content.logging = True

        # set add container
        
        for pair in Config.getSection("Global"): 
            container = Container("cmd", pair[0], "global cmd" )
            container.setUse(self.getState,pair[1])
            self.content.addChild(container)

     

     
    def getState(self, var):
        print "Global getState" , self.use_args
        
        host = self.use_args.split("/")[0]
        domain = self.use_args.split("/")[1]
        print "curl http://" +host + ":8080/" + domain + "/Status/State"
        ret = os.popen("curl http://" + host + ":8080/" + domain + "/Status/State").read()
        return re.sub(r'<[^>]*?>', '', ret).replace("Back","").replace("Result","")
        

    def getRoot(self, text=""):
        string = ""

        res = self.root().__str__()

        return res

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
