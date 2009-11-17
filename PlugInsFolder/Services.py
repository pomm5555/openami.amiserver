import os, re
from AmiTree import Container
from PlugIn import PlugIn
from amiConfig import Config
from Address import *
from EventEngine import *
import urllib2

class Services(PlugIn):

    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"

        #plugin itself
        self.content = Container("plugin", token, "This is a Interface")

        xmlC = Container("cmd", "Xml", "Get the Tree or Subtree as XML", self.getXml)
        xmlC.rendering = Container.PLAIN

        jqC = Container("cmd", "JqHtml", "Get the Tree or Subtree as JQ Touch HTML", self.getJq)
        jqC.rendering = Container.PLAIN

        test = Container("cmd", "test", "Get the Tree or Subtree as JQ Touch HTML", self.test)
        test.rendering = Container.PLAIN

        self.content.addChild(xmlC)
        self.content.addChild(jqC)
        self.content.addChild(test)

    def getXml(self, string=""):
        if not string.__eq__(''):
            address = Address(string).__str__()
            tmp =  EventEngine.root.getByAddress(address).toXml()
            return tmp
        else:
            return EventEngine.root.toXml()


    def getJq(self, string=""):
        if not string.__eq__(''):
            address = Address(string).__str__()
            tmp =  EventEngine.root.getByAddress(address).toJqHtml()
            return tmp
        else:
            return EventEngine.root.toJqHtml()

    def test(self, string=""):



        addr = "http://192.168.178.34:8080/ami.client@jabber.org/Services/JqHtml"
        link = "servant@jabber.org/Status"
        #EventEngine.root.getByAddress(addr).use(link)

        answer = urllib2.urlopen(addr+"?string="+link).read()

        return answer