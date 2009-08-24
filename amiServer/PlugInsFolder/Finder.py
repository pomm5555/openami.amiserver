import os
from AmiTree import Container
from PlugIn import PlugIn

##
# OSX and AppleScript specific plugin that controls some Finder/System functionality
##
class Finder(PlugIn):


    def __init__(self, token, configFile):

        #plugin itself
        self.content = Container("plugin", token, "This is a Finder Plugins")

        # set add container

        self.content.addContainer("cmd","OpenUrl", "open url", self.openUrl)

        self.content.addContainer("cmd", "Unmute", "unmute system", self.unmute)

        self.content.addContainer("cmd", "Mute", "mute system", self.mute)

        self.content.addContainer("cmd", "Restart", "restart system", self.restart)

        self.content.addContainer("cmd", "Sleep", "sleep system", self.sleep)

        self.content.addContainer("cmd", "Shutdown", "shutdown system", self.shutdown)

        self.content.addContainer("cmd", "Say", "say something", self.say)

        self.content.addContainer("cmd", "Beep", "Beep", self.beep)


    def getTree(self):
        return self.content

    def openUrl(self, url="http://www.tuaw.com"):
        os.system("osascript -e 'tell application \"Finder\" to open location \""+url+"\"'" )

    def unmute(self):
        os.system("osascript -e 'set volume output muted false'" )

    def mute(self):
        os.system("osascript -e 'set volume output muted true'" )

    def restart(self):
        os.system("osascript -e 'tell application \"Finder\" to restart'" )

    def sleep(self):
        os.system("osascript -e 'tell application \"Finder\" to sleep'" )

    def shutdown(self):
        os.system("osascript -e 'tell application \"Finder\" to shut down'" )

    def say(self, string="Hello, my name is HAL2000."):
        os.system("osascript -e 'tell application \"Finder\" to say \""+string+"\" using \"Vicki\"'" )

    def beep(self):
        os.system("osascript -e \"beep\"" )