# To change this template, choose Tools | Templates
# and open the template in the editor.
# growlnotify -m "hallo" -t "hallo"


import os, re
from AmiTree import Container
from PlugIn import PlugIn

class Madplay(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"

        #plugin itself
        self.content = MadplayContainer("plugin", token, "This is a Madplay Plugin")

        #Plugin visibility, can be accessed, but is not listed
        self.visible = False
        
        # set add container
        self.content.addContainer("cmd", "Play", "Play Madplay", self.play)

	self.content.addContainer("cmd", "Stop", "Stop Madplay", self.stop)

    def play(self, text=None):
        if not text:
            text="http://munich-radio.de:8000/"
        print "trying to play: >"+str(text)+"<"
        text = self.getText(text)
        print "trying to play:"+text
        if re.match("^http://.*?", text):
            os.system('curl "'+text+'" | madplay -Q - &' )
            return "Playing Stream: "+text
        else:
            os.system("madplay -Q \""+text+"\" &")
            return "Playing File: "+text
        return "what?"

    def stop(self, string=""):
    	os.system('killall madplay')

    # returns the plugin as a tree
    def getTree(self):
        return self.content

    # just a little helper function
    def getText(self, var):
        try:
            var = var.strings["text"]
            return test
        except:
            return var

class MadplayContainer(Container):
    def toJqHtml__(self):

        if self.visible and not self.content == {}:

            result=""
            for k, v in self.content.items():
                result+=v.toJqHtml()

            address = self.getAddress().replace("/", "_").replace("@", "_").replace(".", "_")
            token = self.token

            toolbar = "<div class='toolbar'><h1 style='opacity:1;'>"+token+"</h1><a class='back' href='#'>Back</a></div>"
            items = "<li><a class=\"\" href=\"#edge\">Edge to Edge</a></li>"
            content = '<form action=""><ul>'+items+'</ul></form>'

            html = "<div id='"+address+"'>"+toolbar+content+"</div>"+result

            return html

        else:
            return ""

