
from AmiTree import *
from PlugIn import PlugIn
from CommunicationEngine import CommunicationEngine
from amiConfig import Config
from ctypes import cdll, c_int
from EventEngine import EventEngine
from Address import Address
import time

class SoftKeys(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"

        #plugin itself
        self.content = avrContainer("plugin", token, "This hopefully will be a Threaded SoftKey  Plugin")
        self.content.name = "softKeyThread"
        self.content.start()





    # Functions of the Plugin
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





class avrContainer(ThreadContainer):

    def __init__(self, type, token, information="empty"):
        ThreadContainer.__init__(self, type, token, information="empty")
        self.information = "hehehehe, arschloch"
        self.lastval = 0

        ##
        # Hardware Initialization
        ##
        lib=Config.absPath+"/PlugInsSupport/libavrBridgeC.dylib"
        self.mega=cdll.LoadLibrary(lib)

        self.mega.initUsbLib()

        # init poti
        self.mega.setPortPinDir(1,1,0)
        self.mega.setPortPin(1,1,1)

        # set pins input
        self.mega.setPortPinDir(0,0,0)
        self.mega.setPortPinDir(0,1,0)
        self.mega.setPortPinDir(0,2,0)

        # enable internal pullup
        self.mega.setPortPin(0,0,1)
        self.mega.setPortPin(0,1,1)
        self.mega.setPortPin(0,2,1)

        #LED output
        self.mega.setPortPinDir(2,7,1)

        # light up the led
        self.mega.setPortPin(2,7,1)


    def run(self):
        while True:
            

            #get value from poti
            val = self.mega.getAdcPortPin(1, 1)
            val = (val-30)/738.*100


            #print str(int(val)),
            #print self.mega.getPortPin(0, 0),
            #print self.mega.getPortPin(0, 1),
            #print self.mega.getPortPin(0, 2)


            if self.mega.getPortPin(0,0) == 0:
                self.mega.setPortPin(2,7,1)
                address = Address("/Defaults/Play")
                EventEngine.root.getByAddress(address.__str__()).use("http://www.mondayjazz.com/mixes/mj099_now_just_listen_by_dj_blueprint.mp3")
                time.sleep(.5)

            if self.mega.getPortPin(0,1) == 0:
                self.mega.setPortPin(2,7,0)
                address = Address("/Defaults/Stop")
                EventEngine.root.getByAddress(address.__str__()).use()
                time.sleep(.5)

            if not str(int(self.lastval)).__eq__(str(int(val))):
                print "Default Volume"+str(val)+", "+str(int(self.lastval))+", "+str(int(val))
                address = Address("/Defaults/SetVol")
                print EventEngine.root.getByAddress(address.__str__())
                EventEngine.root.getByAddress(address.__str__()).use(val)
                self.lastval = val


            time.sleep(.3)

