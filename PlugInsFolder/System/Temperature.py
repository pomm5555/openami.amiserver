# -*- coding: utf-8 -*-

import os
import simplejson as json
from AmiTree import Container
from PlugIn import PlugIn

##
# OSX and AppleScript specific plugin that controls some Finder/System functionality
##
class Temperature(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "macos"

        #plugin itself
        self.content = Container("plugin", token, 'Temperature Plugin')
        
        temp = Container("cmd","LivingRoom", '0.5', self.get)
        temp.rendering = Container.PLAIN
        
        # set add container

        self.content.addChild(temp)


    def get(self, string=""):
        self.information =  str(float(self.information)+0.7)
        #return self.information
        return self.information+" &#176;C"