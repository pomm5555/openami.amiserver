
from AmiTree import *
from PlugIn import PlugIn
from amiConfig import Config
from EventEngine import EventEngine
from Address import Address
import time, socket

class FritzMonitor(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        # set plugins "hardware" architecture for system dependencies
        self.architecture = "all"

        # create plugin itself
        self.content = callmonitorContainer("plugin", token, "This hopefully will be a Call Monitor SoftKey  Plugin")

        # dont know wheather it works, shold set the name of the thread
        self.content.name = "CallMonitorThread"

        # start thread
        self.content.start()


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




class callmonitorContainer(ThreadContainer):

    def simpleHandler(self, d):

        address = Address("/Defaults/Notification")

        """a very simple handler for incoming calls, prints to stdout"""
        if d[1] == 'RING':
            print 'Incoming call from: %s to: %s' % (d[3], d[4])
            EventEngine.root.getByAddress(address.__str__()).use('Incoming call from: %s to: %s' % (d[3], d[4]))
        elif d[1] == 'CALL':
            print 'Outgoing call from: %s to: %s via: %s' % (d[4], d[5], d[6])
            EventEngine.root.getByAddress(address.__str__()).use('Outgoing call from: %s to: %s via: %s' % (d[4], d[5], d[6]))
        elif d[1] == 'DISCONNECT':
            print 'Call ended!'
            #EventEngine.root.getByAddress(address.__str__()).use('Call ended!')

        self.log.append("<br/>\n"+d.__str__())

    def __init__(self, type, token, information="empty"):
        ThreadContainer.__init__(self, type, token, information="empty")
        self.information = "hehehehe, callmonitor"
        self.handler = self.simpleHandler

        self.log = []
        self.log.append("Call Monitor Log:")



    def run(self):
        host='fritz.box'
        port=1012
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        while 1:
            line = s.recv(1024)
            if not line:
                break
            self.handler(line.strip().split(';'))
            time.sleep(1)
        s.close()

    def toHtml(self):
        if self.visible:
            result=""
            for k, v in self.content.items():
                result+=v.toHtml()

            #if result.__eq__(""):
            #    return "<li><a href=\""+self.getAddress()+"\">"+self.token+"</a>"+result+"</li>"
            return "<ul><li><a href=\""+self.getAddress()+"\">"+self.token+"</a> L</li>"+result+"</ul>"
            
        else:
            return ""

    def use(self, string=""):
        result = ""
        for elem in self.log:
            result += "\n"+elem
        return result