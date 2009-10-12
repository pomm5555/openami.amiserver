from EventProcessing import Behavior
import os, re
from AmiTree import Container
from PlugIn import PlugIn
from amiConfig import Config
from EventProcessing import *

class Filesystem(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"


        #plugin itself
        self.content = Container("plugin", token, "Filesystem Plugin")

        # load all items from config
        for pair in Config.getSection("Filesystem"):
            print "+-+"+Config.absPath
            print pair[0], pair[1]
            self.loadFilesystem(pair)
            

    def file(self, string=""):

        if re.match(".*?\.mp3", self.information):
            return Formatter.ajax("MP3", Behavior.audio(self.information))

        if re.match(".*?\.log", self.information) or re.match(".*?\.properties", self.information):
            return Formatter.ajax("TXT", Behavior.text(self.information))

        else:
            return Behavior.text(self.information)


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


    def loadFilesystem(self, pair):
        #for files
        if not (os.path.isdir(Config.absPath+"/"+pair[1])):
            self.content.addContainer("cmd", pair[0], Config.absPath+"/"+pair[1], self.file)
        #for folders
        else:
            tmp = Container("cmd", pair[0], Config.absPath+"/"+pair[1])
            tmp.addChildList(self.loadFilesystemFolder(Config.absPath+"/"+pair[1]))
            self.content.addChild(tmp)


    # recursive plugin finder
    def loadFilesystemFolder(self, Path):

        # get all elements in folder into list
        folder =  os.listdir(Path)
        print folder

        result = []

        for elem in folder:
            # add folders as plugin
            # if dir
            print Path+"/"+elem
            if os.path.isdir(Path+"/"+elem):
                print "### loding folder: "+elem
                tmpcont = Container("folder", elem, "this is the tree representation of a folder")
                tmpcont.addChildList(self.loadFilesystemFolder(Path+"/"+elem))
                result.append(tmpcont)
            #if file
            else:
                print "### adding file: "+Path+"/"+elem
                result.append(Container("cmd", elem, Path+"/"+elem, self.file))
                
        return result
