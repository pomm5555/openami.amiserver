import os
from AmiTree import Container
from PlugIn import PlugIn

##
# OSX and AppleScript specific plugin that controls some Finder/System functionality
##
class Finder(PlugIn):


    def __init__(self, token, configFile):

        #plugin itself
        self.content = Container(token, "This is a Finder Plugins")

        # set add container

        self.content.addContainer("OpenUrl", "open url", self.openUrl)

        self.content.addContainer("Unmute", "unmute system", self.unmute)

        self.content.addContainer("Mute", "mute system", self.mute)

        self.content.addContainer("Restart", "restart system", self.restart)

        self.content.addContainer("Sleep", "sleep system", self.sleep)

        self.content.addContainer("Shutdown", "shutdown system", self.shutdown)

        self.content.addContainer("Say", "say something", self.say)

        self.content.addContainer("Beep", "Beep", self.beep)


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
        print string.strings["text"]
        os.system("osascript -e 'tell application \"Finder\" to say \""+string.strings["text"]+"\" using \"Vicki\"'" )

    def beep(self):
        os.system("osascript -e \"beep\"" )