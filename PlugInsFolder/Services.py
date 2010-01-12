import os, re
from AmiTree import Container
from PlugIn import PlugIn
from amiConfig import Config
from Address import *
from EventEngine import *
import urllib2
import simplejson as json

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

        multirequest = Container("cmd", "multirequest", "Access multiple requests with one request, function returns some JSON code, or should", self.mreq)
        multirequest.rendering = Container.PLAIN


        self.content.addChild(xmlC)
        self.content.addChild(jqC)
        self.content.addChild(multirequest)

    def getXml(self, string=""):
        if not string.__eq__(''):
            v
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

    def mreq(self, string=''):
        #print string
        requests = json.loads(string)
        #print requests
        
        result = {}
        for key, request in requests.items():
            request = Address(request)
            result[key]=self.root().getByAddress(request.__str__()).use()
        return json.dumps(result)