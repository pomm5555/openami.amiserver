import os
from AmiTree import Container
from PlugIn import PlugIn
from Address import Address
from amiConfig import Config
from EventEngine import EventEngine

class Defaults(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"
        self.override_dict ={}
        self.jid = Config.get("jabber","jid")
        global backend
        backend = Config.get("Defaults","backend")
        global scenario
        scenario = "default"
        #plugin itself
        self.content = Container("plugin", token, "This is a Defaults Plugin")
        self.content.addContainer("cmd","getBackend","getBackend", self.getBackend)
        for pair in Config.getSection("Defaults"):
            if pair[0].endswith('_plain'):
                title= pair[0].replace('_plain','')
                container = Container("cmd",title,pair[1],self.general)
                container.rendering = Container.PLAIN
            else:
                container = Container("cmd",pair[0],pair[1],self.general)
                container.setUseArgs(backend)
            self.content.addChild(container)
            
            #self.content.addContainer("cmd", pair[0], pair[1], use=self.general, args="test")
            
        self.content.addContainer("cmd","set","set",self.override)
        self.content.addContainer("cmd","setScenario","set a Scenario", self.setScenario)
        self.content.addContainer("cmd","getScenario", "get current Scenario", self.getScenario)
        
    def setScenario(self, var):
        print "\n **** Scenario set to: " , var
        global scenario
        
        if scenario == 'default':
            newaddr = Address('/Scenarios/'+var+'/toggleState')
            EventEngine.root.getByAddress(newaddr.__str__()).use()
        elif var == 'default':
            oldaddr = Address('/Scenarios/'+scenario+'/toggleState')
            EventEngine.root.getByAddress(oldaddr.__str__()).use()        
        else:
            newaddr = Address('/Scenarios/'+var+'/toggleState')
            EventEngine.root.getByAddress(newaddr.__str__()).use()
            oldaddr = Address('/Scenarios/'+scenario+'/toggleState')
            EventEngine.root.getByAddress(oldaddr.__str__()).use()
       
        scenario = var
        
    def getScenario(self,var):
        global scenario
        return scenario
        
    def getBackend(self,var):
        global backend
        return backend
    
    def override(self,var):
        #self.getParent().addContainer("cmd",var,var,None)
        print "\n ****", self , var 
        global backend
        backend = var
        
        for addr in self.getParent().getAddressList():
            a = Address("/"+addr)
            info = EventEngine.root.getByAddress(a.__str__()).information
            if "Boxee" in info: 
                repl = "Boxee"
            elif "Madplay" in info:
                repl = "Madplay"
            elif "LastFM" in info:
                repl = "LastFM"
            else:
                pass    
            EventEngine.root.getByAddress(a.__str__()).information = info.replace(repl,var)
            
        
    def general(self, string=None):
        address = Address(self.information)

        
        if not string:
          #  return EventEngine.root.getByAddress(
            return EventEngine.root.getByAddress(address.__str__()).use()
        
        string = self.getText(string)
    	return EventEngine.root.getByAddress(address.__str__()).use(string)

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