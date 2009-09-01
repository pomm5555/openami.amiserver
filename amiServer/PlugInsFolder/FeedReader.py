# To change this template, choose Tools | Templates
# and open the template in the editor.
# growlnotify -m "hallo" -t "hallo"


import os, time, urllib2
from AmiTree import *
from PlugIn import PlugIn

class FeedReader(PlugIn):


    def __init__(self, token, configFile):

        #plugin itself, is threaded uses the its process method
        self.content = ThreadContainer("plugin", token, "This hopefully will be a Threaded Feedreader Plugin")
        self.content.setDo(self.process)
        self.content.start()
        #self.content.setUse(self.use)


    def process(self, url="http://www.google.de"):
        while True:
            print "Hey, where is the feed?"
            req = urllib2.Request(url=url)
            f = urllib2.urlopen(req)
            self.content.inforamtion = f.read()
            time.sleep(10)

    # returns the plugin as a tree
    def getTree(self):
        return self.content

    def use(self, test):
        return "+"+self.content.information

    # just a little helper function
    def getText(self, var):
        try:
            var = var.strings["text"]
            return test
        except:
            return var