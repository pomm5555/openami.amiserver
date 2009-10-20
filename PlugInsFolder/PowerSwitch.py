import os, re
from AmiTree import Container
from PlugIn import PlugIn
from amiConfig import Config

class PowerSwitch(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"

        #plugin itself
        self.content = PowerSwitchContainer("plugin", token, "This is a Powerswitch Interface")

        self.content.addContainer("cmd", "test", "informatio")


class PowerSwitchContainer(Container):

    def toJqHtml(self):

        if self.visible and not self.content == {}:

            result=""
            for k, v in self.content.items():
                result+=v.toJqHtml()

            address = self.getAddress().replace("/", "_").replace("@", "_").replace(".", "_")
            token = self.token

            on=Config.jid+'/Defaults/audioplay'
            off=Config.jid+'/Defaults/audiostop'

            toolbar = '<div class="toolbar"><h1>'+token+'</h1><a class="back" href="#">Back</a></div>'
            content = '<ul><li>Lamp 1<span class="toggle"><input type="checkbox" onChange="if(this.checked) $.get(\''+on+'\');else $.get(\''+off+'\');"/></span></li></ul>'
                                                                            #if(this.checked)alert(\'hallo\')
            html = "<div id='"+address+"'>"+toolbar+content+"</div>"+result

            return html

        else:
            return ""