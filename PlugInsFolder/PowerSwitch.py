import os, re
from AmiTree import Container, SwitchContainer, TextfieldContainer
from PlugIn import PlugIn
from amiConfig import Config

class PowerSwitch(PlugIn):

    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"

        #plugin itself
        self.content = Container("plugin", token, "This is a GEneric Interface")

        switch = SwitchContainer("cmd", "MunichRadio", "This is a Switch Interface",
                                        on=Config.jid+'/Defaults/audioplay',
                                        off=Config.jid+'/Defaults/audiostop')
        self.content.addChild(switch)

        switch = SwitchContainer("cmd", "MunichRadio2tet", "This is a Switch Interface",
                                        on=Config.jid+'/Defaults/audioplay',
                                        off=Config.jid+'/Defaults/audiostop')

        self.content.addChild(switch)

        text = TextfieldContainer("cmd", "Volume", "This is a Volume Textfield",
                                        target=Config.jid+"/Defaults/setvol")

        self.content.addChild(text)