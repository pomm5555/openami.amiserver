# To change this template, choose Tools | Templates
# and open the template in the editor.
import os
from AmiTree import Container
from PlugIn import PlugIn
import ConfigParser

#Plugin convention: the class name must equal its filename
class iTunes(PlugIn):

    def __init__(self, token, configFile):
        self.configFile = configFile
        self.parseConfig()

        #plugin itself
        self.content = Container(token, "This is a iTunes Plugins")

        # play functionality
        self.content.addChild("Play", Container("Play", "Play iTunes"))
        self.content.getChild("Play").setUse(self.play)

        # pause functionality
        self.content.addChild("Pause", Container("Pause", "Pause iTunes"))
        self.content.getChild("Pause").setUse(self.pause)

        # next functionality
        self.content.addChild("Next", Container("Next", "Next iTunes Track"))
        self.content.getChild("Next").setUse(self.next)

        # prev functionality
        self.content.addChild("Prev", Container("Prev", "Prev iTunes Track"))
        self.content.getChild("Prev").setUse(self.prev)

        # vol up functionality
        self.content.addChild("VolUp", Container("VolUp", "VolUp iTunes"))
        self.content.getChild("VolUp").setUse(self.vol_up)

        # vol down functionality
        self.content.addChild("VolDown", Container("VolDown", "VolDown iTunes"))
        self.content.getChild("VolDown").setUse(self.vol_down)

        # stop functionality
        self.content.addChild("Stop", Container("Stop", "Stop iTunes"))
        self.content.getChild("Stop").setUse(self.stop)

        # mute functionality
        self.content.addChild("Mute", Container("Mute", "Mute iTunes"))
        self.content.getChild("Mute").setUse(self.mute)

        # unmute functionality
        self.content.addChild("Unmute", Container("Unmute", "Unmute iTunes"))
        self.content.getChild("Unmute").setUse(self.unmute)


    def getTree(self):
        return self.content

    def unmute(self):
        os.system(self.iTunesScript+" unmute")

    def mute(self):
        os.system(self.iTunesScript+" mute")

    def play(self):
        os.system(self.iTunesScript+" play")

    def pause(self):
        os.system(self.iTunesScript+" pause")

    def next(self):
        os.system(self.iTunesScript+" next")

    def prev(self):
        os.system(self.iTunesScript+" prev")

    def vol_up(self):
        os.system(self.iTunesScript+" vol up")

    def vol_down(self):
        os.system(self.iTunesScript+" vol down")

    def stop(self):
        os.system(self.iTunesScript+" stop")

    def parseConfig(self):
        config = ConfigParser.ConfigParser()
        config.readfp(open(self.configFile))
        # nicht vergessen, try catch block wieder einbauen


        # parsing jabber section
        self.iTunesScript = config.get('iTunes', 'ScriptPath')
