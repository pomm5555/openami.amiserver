import xml.sax as sax
from AmiTree import *
from PlugIn import PlugIn
import urllib, time
from EventEngine import EventEngine
from Address import Address


class FeedReader(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"

        #plugin itself, is threaded uses the its process method
        self.content = ThreadContainer("plugin", token, "This hopefully will be a Threaded Feedreader Plugin")
        self.content.setDo(self.process)

        self.content.start()

        #self.content.setUse(self.use)


    def process(self, url="http://www.mondayjazz.com/mj.xml"):
        while True:
            print "parsing: "+url
            xml = urllib.urlopen(url)
            handler = PodcastHandler()
            parser = sax.make_parser()
            parser.setContentHandler(handler)
            parser.parse(xml)

            address = Address("/FeedReader") # TODO should already know its address
            feedreader = EventEngine.root.getByAddress(address.__str__())

            for k, v in handler.links.items():
                
                if not feedreader.content.has_key(k):
                    print k,v

                    feedreader.addChild(FeedLeafContainer("cmd", k, v))
                    # address = Address("/FeedReader/"+str(i))
                    # print "#####" + EventEngine.root.getByAddress("/FeedReader").token

            time.sleep(60*60) #every hours or so



    # returns the plugin as a tree
    def getTree(self):
        return self.content

    def use(self, test=""):
        return "+"+self.content.information

    # just a little helper function
    def getText(self, var):
        try:
            var = var.strings["text"]
            return test
        except:
            return var


class FeedLeafContainer(Container):
    def use(self, str=None):
        address = Address("/Defaults/Play") 
        EventEngine.root.getByAddress(address.__str__()).use(self.information)



class PodcastHandler(sax.handler.ContentHandler):

    def __init__(self):
        self.links = {}
        self.lastTitle = ""

    def startElement(self, name, attrs):
        self.tag=name;


    def endElement(self,name):
        pass

    def characters(self,data):

        if not data.strip().__eq__("") and self.tag.__eq__("title"):
            self.lastTitle = data

        if not data.strip().__eq__("") and self.tag.__eq__("guid"):
            self.links[self.lastTitle]=data

    def load(self, data):
        handler = PodcastHandler()
        parser = sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(data)
        return self.links





