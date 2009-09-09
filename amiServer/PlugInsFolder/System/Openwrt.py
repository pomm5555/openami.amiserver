import os
from AmiTree import Container
from PlugIn import PlugIn

##
# OSX and AppleScript specific plugin that controls some Finder/System functionality
##
class Openwrt(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"

        #plugin itself
        self.content = Container("plugin", token, "This is a Finder Plugins")

        # set add container

        self.content.addContainer("cmd","SetVol", "set system volume via amixer", self.setVol)
        self.content.addContainer("cmd","Kernel", "get Kernel Infos", self.kernelInfo)



    def getTree(self):
        return self.content

    def setVol(self, vol="0"):
        vol = self.getText(vol)
        print "new amixer volume:"+vol
        os.system("amixer sset Speaker "+vol+"%" )

    def kernelInfo(self, string=""):
        result = ""
        for elem in os.uname():
            result+=elem+"\n"
        return result


    def getText(self, var):
        try:
            var = var.strings["text"]
            return test
        except:
            return var