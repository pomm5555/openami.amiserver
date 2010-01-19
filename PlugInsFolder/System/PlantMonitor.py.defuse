from AmiTree import *
from PlugIn import PlugIn
from amiConfig import Config
from ctypes import cdll, c_int
from EventEngine import EventEngine
from Address import Address
import time


class PlantMonitor(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "macos"


        if self.architecture.__eq__(Config.get("server", "architecture")):

            # plugin itself
            self.content = avrContainer("plugin", token, "This hopefully will be a Threaded SoftKey  Plugin")
            self.content.rendering = Container.PLAIN
            self.content.start()

        else:
            self.content = Container("plugin", token, "not supported")




class avrContainer(ThreadContainer):

    def __init__(self, type, token, information="empty"):
        ThreadContainer.__init__(self, type, token, information="empty")
        self.lastval = 0
        self.information = information

        ##
        # Hardware Initialization
        ##

        if True: #try:
            lib=Config.absPath+Config.get("avrBridge", "lib")
	    #print lib
            self.mega=cdll.LoadLibrary(lib)
            self.mega.initUsbLib()
            self.port = 1



            #print '!-!-!-!-! PLANTMONITOR sucessfully initialized'

            for tuple in Config.getSection("Plantmonitor"):
                tmpcont = Container("plugin", tuple[0], tuple[1])
                tmpcont.pin = tuple[1]
                tmpcont.setUse(self.leafuse)

                self.mega.setPortPinDir(self.port,tmpcont.pin,0)
                self.mega.setPortPin(self.port,tmpcont.pin,1)

                self.addChild(tmpcont)


#        except Exception,e:
#            print "[PLANTMONITOR ERROR] Could not init plugin\n"+str(e)







    def run(self):
        while True:
            #get value from poti
            for token, container in self.content.items():
                val = self.mega.getAdcPortPin(self.port,int(container.pin))
                val = (val-30)/738.*100
                container.information = val
            time.sleep(1)


    def use(self, text):
        return self.information

    def leafuse(self, text):
        return str(int(self.information))+'%'
