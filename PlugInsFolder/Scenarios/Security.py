from Address import Address
from AmiTree import Container
from PlugIn import PlugIn
from xmppEngine import XMPPEngine
from EventEngine import EventEngine
import os
import time

class Security(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"

        global active
        global lastMotion
        lastMotion = ""
        active=False
        
        #plugin itself
        self.content = Container("plugin", token, "Security Scenario")
        self.content.logging = True

        # set add container
        
        self.content.addContainer("cmd","State", "get Security State", self.getState)
        self.content.addContainer("cmd","TriggerMotion","Trigger Motion event", self.triggerMotion)
        self.content.addContainer("cmd","LastMotion","Last Motion event", self.lastMotion)
        self.content.addContainer("cmd","setState", "set State", self.setState)
        self.content.addContainer("cmd","toggleState", "toggleState", self.toggleState)
        
    def triggerMotion(self,var):
        global lastMotion
        global active
        lastMotion = time.ctime()
        print "\n *********** ", lastMotion , " Motion Event Received - State: ", active     
        
        if active:
            #print(dir(EventEngine.root))
            addr = Address('/Defaults/notification')
            EventEngine.root.getByAddress(addr.__str__()).use('[openAMI] - Security Alert - Motion detected at: '+lastMotion)
            #os.system('madplay /Volumes/DEV/workspace/tmp/siren_1.mp3')
            os.system('madplay /Volumes/DEV/workspace/tmp/sec0.mp3 /Volumes/DEV/workspace/tmp/sec1.mp3')
            
    def lastMotion(self,var):
        print "\n *********** ", lastMotion , " LastMotion Requested"
        return lastMotion
        
    def getState(self, var):
        global active
        return active
    
    def toggleState(self,var):
        global active
        if active:
            active = False
        else:
            active = True
        print "\n **** toggled State ", self.getParent() ,' - now: ' , active
    
    def setState(self,var):
        global active
        active = var
           
    def activate(self,var):
        global active
        active = True
        
    def deactivate(sel,var):
        global active
        active = False
        

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
