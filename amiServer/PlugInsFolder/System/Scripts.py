import os
from AmiTree import Container
from PlugIn import PlugIn

##
# OSX and AppleScript specific plugin that controls some Finder/System functionality
##
class Scripts(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "macos"

        #plugin itself
        self.content = Container("plugin", token, "This is a Scripts Plugins")

        # set add container

        self.content.addContainer("cmd","AppleScript", "apple a script", self.appleScript)


    def getTree(self):
        return self.content

    def appleScript(self, script="tell application \"Finder\" to say \"Hi, I am the AppleScript PlugIn\" using \"Vicki\""):
        script = self.getText(script)
        command = "osascript -e '"+script+"'"
        print command
        os.system(command)


    def getText(self, var):
        try:
            var = var.strings["text"]
            return var
        except:
            return var