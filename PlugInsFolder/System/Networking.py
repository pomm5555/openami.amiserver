# -*- coding: utf-8 -*-

from AmiTree import *
from PlugIn import PlugIn
from amiConfig import Config
from EventEngine import EventEngine
from Address import Address
import time, socket, urllib2

class Networking(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        # set plugins "hardware" architecture for system dependencies
        self.architecture = "all"

        # create plugin itself
        self.content = ThreadContainer("plugin", token, "Listening to Broadcasts for Client amiServers")
        
        if Config.get("server", "master").__eq__("on"):
            method = self.listen
            ThreadName = "ClientListener"
        else:
            method = self.send
            ThreadName = "Broadcaster"
            
            
        self.content.setDo(method)
        # dont know wheather it works, shold set the name of the thread
        self.content.name = ThreadName

        # start thread
        self.content.start()


    def listen(self):
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        my_socket.bind(('', 8081))
    
        print 'start ClientListener ...'
    
        while True :
            clientName , remoteIp = my_socket.recvfrom(8192)
            print 'message (%s) from : %s' % (str(clientName), remoteIp[0])
            self.root().addChild(WebBuddyContainer("remoteInstanceView", clientName, remoteIp[0]))
            
            
    def send(self):
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print 'start Broadcasting ...'
    
        while True :
            my_socket.sendto(Config.get("server", "token"), ('<broadcast>' , 8081))
            time.sleep(60)


    def toHtml(self):
        if self.visible:
            result = ""
            for k, v in self.content.items():
                result += v.toHtml()

            #if result.__eq__(""):
            #    return "<li><a href=\""+self.getAddress()+"\">"+self.token+"</a>"+result+"</li>"
            return "<ul><li><a href=\"" + self.getAddress() + "\">" + self.token + "</a> L</li>" + result + "</ul>"
            
        else:
            return ""

    def usemethod(self, string=""):
        result = ""
        for elem in self.log:
            result += "\n" + elem
        return result
    
class WebBuddyContainer(Container):
    def __init__(self, type, token, information):
        Container.__init__(self, type, token, information)
        self.rendering = Container.PLAIN
        self.request = None
        addr = "http://" + self.information + ":8080/" + self.token + "/Services/JqHtml" + "?string=" + self.token
        print addr
        self.webcontent = urllib2.urlopen(addr).read()
        print self.webcontent
        
    def getByAddress(self, address):
        #print "+++++"+address
        print address
        self.request = address
        return self
    
    def toJqHtmlElement(self):
        if self.visible:
            content = "<li class='arrow'><a target='_self' href='"+self.getAddress()+"'><img src='/"+Config.get("server", "token")+"/Filesystem/html/images/amiNetwork.png' />"+self.token+"</a></li>"
            return content
        else:
            return ""
    def use(self, msg=""):
        if self.request:
            print ">>>>>>>"+self.request
            print self.information
            print self.token
            print "#######"+self.webcontent
            
            return urllib2.urlopen("http://"+self.information+":8080/"+self.token+"/"+self.request).read()
        else:
            return self.webcontent  
    
