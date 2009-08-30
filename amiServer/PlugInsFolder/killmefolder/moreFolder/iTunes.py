# To change this template, choose Tools | Templates
# and open the template in the editor.
import os
from AmiTree import Container
from PlugIn import PlugIn
import ConfigParser
from amiConfig import Config

#Plugin convention: the class name must equal its filename
class iTunes(PlugIn):

    def __init__(self, token, configFile):
        self.configFile = configFile
        self.parseConfig()

        #plugin itself
        self.content = Container("plugin",token, "This is a iTunes Plugins")

        # play functionality
        self.content.addChild(Container("cmd", "Play", "Play iTunes"))
        self.content.getChild("Play").setUse(self.play)

        # pause functionality
        self.content.addChild(Container("cmd","Pause", "Pause iTunes"))
        self.content.getChild("Pause").setUse(self.pause)

        # next functionality
        self.content.addChild(Container("cmd","Next", "Next iTunes Track"))
        self.content.getChild("Next").setUse(self.next)

        # prev functionality
        self.content.addChild(Container("cmd","Prev", "Prev iTunes Track"))
        self.content.getChild("Prev").setUse(self.prev)

        # vol up functionality
        self.content.addChild(Container("cmd","VolUp", "VolUp iTunes"))
        self.content.getChild("VolUp").setUse(self.vol_up)

        # vol down functionality
        self.content.addChild(Container("cmd","VolDown", "VolDown iTunes"))
        self.content.getChild("VolDown").setUse(self.vol_down)

        # stop functionality
        self.content.addChild(Container("cmd","Stop", "Stop iTunes"))
        self.content.getChild("Stop").setUse(self.stop)

        # mute functionality
        self.content.addChild(Container("cmd","Mute", "Mute iTunes"))
        self.content.getChild("Mute").setUse(self.mute)

        # unmute functionality
        self.content.addChild(Container("cmd","Unmute", "Unmute iTunes"))
        self.content.getChild("Unmute").setUse(self.unmute)


    def getTree(self):
        return self.content

    def unmute(self, string=""):
        os.system(self.iTunesScript+" unmute")

    def mute(self, string=""):
        os.system(self.iTunesScript+" mute")

    def play(self, string=""):
        os.system(self.iTunesScript+" play")

    def pause(self, string=""):
        os.system(self.iTunesScript+" pause")

    def next(self, string=""):
        os.system(self.iTunesScript+" next")

    def prev(self, string=""):
        os.system(self.iTunesScript+" prev")

    def vol_up(self, string=""):
        os.system(self.iTunesScript+" vol up")

    def vol_down(self, string=""):
        os.system(self.iTunesScript+" vol down")

    def stop(self, string=""):
        os.system(self.iTunesScript+" stop")

    def parseConfig(self):

        # parsing jabber section
        self.iTunesScript = Config.iTunesScript
