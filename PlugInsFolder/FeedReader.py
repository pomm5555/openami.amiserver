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
        self.content.setUse(self.display)

        # this line should be read from config file
        #podcasts = Config.podcasts.split(",")
        for touple in Config.getSection("FeedReader"):
            #t = touple.split(">")
            tmpcont = Container("plugin", touple[0], touple[1])
            tmpcont.setUse(self.display)
            self.content.addChild(tmpcont)

        self.content.addContainer("cmd", "Random", "/FeedReader/mondayjazz", self.playRandom)

        self.content.start()


        #self.content.setUse(self.use)


    def process(self):
        time.sleep(5)
        while True:

            for tk, feed in self.content.items():

                if not tk.__eq__("Random"):

                    print "parsing: "+tk

                    try:
                        xml = urllib.urlopen(feed.information)
                        handler = PodcastHandler()
                        parser = sax.make_parser()
                        parser.setContentHandler(handler)
                        parser.parse(xml)


                        #get Podcast Container
                        podcastContainer = EventEngine.root.getByAddress(feed.getAddress())

                        for k, v in handler.links.items():

                            if not podcastContainer.content.has_key(k.replace(" ", "_")):
                                k = k.encode( "utf-8" )
                                v = v.encode( "utf-8" )
                                print k,v

                                podcastContainer.addChild(FeedLeafContainer("cmd", k, v))
                                # address = Address("/FeedReader/"+str(i))
                                # print "#####" + EventEngine.root.getByAddress("/FeedReader").token
                            else:
                                pass

                    except:
                        xml = ""
                        print "[URLLIB ERROR]"


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


    def display(self, string=""):
        return self.toHtml()
            
    def use(self, test=""):
        return self.toHtml()

    # just a little helper function
    def getText(self, var):
        try:
            var = var.strings["text"]
            return test
        except:
            return var


class FeedLeafContainer(Container):
    def use(self, str=None):
        address = Address("/Defaults/audioplay")
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
