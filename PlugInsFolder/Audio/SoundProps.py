import os
from AmiTree import Container
from PlugIn import PlugIn


class SoundProps(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"

        #plugin itself
        self.content = Container("plugin", token, "Set sound properties like volume.")

        # set add container

        self.content.addContainer("cmd","SetVol", "set system volume via amixer", self.setVol)


    def setVol(self, vol="0"):
        vol = self.getText(vol)
        print "new amixer volume:"+str(vol)
        os.system("amixer sset Speaker "+str(vol)+"%" )