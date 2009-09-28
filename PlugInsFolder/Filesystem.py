import os.path
import os
from AmiTree import Container
from PlugIn import PlugIn
from Address import Address
from amiConfig import Config

class Filesystem(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"


        #plugin itself
        self.content = Container("plugin", token, "Filesystem Plugin")

        # load all items from config
        for pair in Config.getSection("Filesystem"):
            print pair[0], pair[1]
            self.loadFilesystem(pair)
            

    def file(self, string=""):
        f =  open(self.information)
        return f.read()


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
        if not (os.path.isdir(pair[1])):
            self.content.addContainer("cmd", pair[0], pair[1], self.file)
        #for folders
        else:
            tmp = Container("cmd", pair[0], pair[1])
            tmp.addChildList(self.loadFilesystemFolder(pair[1]))
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
            print Config.absPath+"/"+Path+"/"+elem
            if os.path.isdir(Config.absPath+"/"+Path+"/"+elem):
                print "### loding folder: "+Path+"/"+elem
                tmpcont = Container("folder", elem, "this is the tree representation of a folder")
                tmpcont.addChildList(self.loadFilesystemFolder(Path+"/"+elem))
                result.append(tmpcont)
            #if file
            else:
                print "### adding file: "+Config.absPath+"/"+elem
                result.append(Container("cmd", elem, Config.absPath+"/"+Path+"/"+elem, self.file))
                
        return result
