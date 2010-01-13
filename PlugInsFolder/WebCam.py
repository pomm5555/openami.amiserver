
from AmiTree import Container
from PlugIn import PlugIn
from xmppEngine import XMPPEngine
import os

class WebCam(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"


        #plugin itself
        self.content = WebCamContainer("plugin", token, "This is a Webcam Plugin")
        self.content.logging = True

        # set add container
        self.content.addContainer("cmd", "TakePicture", "TakePicture", self.takePic)
        
	

    def takePic(self, var=""):
	os.system("/Users/ka010/share/workspace/python/amiServer/PlugInsSupport/./takepic.sh")

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

class WebCamContainer(Container):

    def toJqHtml(self):

        if self.visible and not self.content == {}:

            result=""
            for k, v in self.content.items():
                result+=v.toJqHtml()

            address = self.getAddress().replace("/", "_").replace("@", "_").replace(".", "_")
            token = self.token

	
            iframe = ""#"<iframe src='http://192.168.1.239:8081' width='300' height='240' scrolling='no'></iframe>"

            toolbar = '<div class="toolbar"><h1>'+token+'</h1><a class="back" href="#">Back</a></div>'
                                     
            html = "<div id='"+address+"'>"+toolbar+iframe+"</div>"+result

            return html

        else:
            return ""
