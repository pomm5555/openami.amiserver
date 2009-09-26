import xml.sax as sax
from AmiTree import *
from PlugIn import PlugIn
import urllib, time, random
from EventEngine import EventEngine
from Address import Address
from amiConfig import Config


class FeedReader(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"

        #plugin itself, is threaded uses the its process method
        self.content = ThreadContainer("plugin", token, "This hopefully will be a Threaded Feedreader Plugin") #ThreadContainer
        self.content.setDo(self.process)

        # this line should be read from config file
        podcasts = Config.podcasts.split(",")
        for touple in podcasts:
            t = touple.split(">")
            self.content.addChild(Container("plugin", t[0], t[1]))

        self.content.addContainer("cmd", "Random", "/FeedReader/MondayJazz", self.playRandom)


        self.content.start()


        #self.content.setUse(self.use)


    def process(self):
        time.sleep(5)
        while True:
            #print "parsing: "+url
            #print "COME ON!!!!! "+self.getAddress() ## should not echo NONE or something
            #print "COME ON!!!!! "+self.root().__str__() ## should not echo NONE or something


            for tk, feed in self.content.items():

                if not tk.__eq__("Random"):

                    print "parsing: "+tk

                    xml = urllib.urlopen(feed.information)
                    handler = PodcastHandler()
                    parser = sax.make_parser()
                    parser.setContentHandler(handler)
                    parser.parse(xml)

                    #get Podcast Container
                    podcastContainer = EventEngine.root.getByAddress(feed.getAddress())

                    for k, v in handler.links.items():

                        if not podcastContainer.content.has_key(k.replace(" ", "_")):
                            print k,v

                            podcastContainer.addChild(FeedLeafContainer("cmd", k, v))
                            # address = Address("/FeedReader/"+str(i))
                            # print "#####" + EventEngine.root.getByAddress("/FeedReader").token
                        else:
                            pass

            time.sleep(60*60) #every hour or so



    def playRandom(self, string=""):
        address = Address(self.information)
        data = EventEngine.root.getByAddress(address.__str__()).content.items()
        print data
        elem = None

        if data != []:
            index = random.randint(0, len(data) - 1)
            elem = data[index]

        if elem:
            print elem
            elem[1].use()
            
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
        if not name.strip().__eq__("") and self.tag.__eq__("enclosure"):
            self.links[self.lastTitle]=attrs["url"]

    def endElement(self,name):
        pass

    def characters(self,data):

        if not data.strip().__eq__("") and self.tag.__eq__("title"):
            self.lastTitle = data

        #if not data.strip().__eq__("") and self.tag.__eq__("enclosure"):
        #    self.links[self.lastTitle]=data

    def load(self, data):
        handler = PodcastHandler()
        parser = sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(data)
        return self.links