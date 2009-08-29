# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="markus"
__date__ ="$Aug 20, 2009 12:22:08 AM$"
from AmiTree import Container
import os

class PlugIns:

    def __init__(self, pluginsFolder, configFile):

        self.pluginsFolder = pluginsFolder


        # create root container
        self.root = Container("tmp", "tmptoken", "tmpinformation")

        #print os.path.walk("./"+pluginsFolder, None, "None")

        # Load plugins from folder
        pluginFiles =  os.listdir("./"+pluginsFolder)
        i=0
        for elem in pluginFiles:
            if elem[-3:].__eq__(".py") and not (elem[:1].__eq__("_")):
                print "loading: "+ elem
                #print("from "+pluginsFolder+"."+elem[:-3]+" import "+elem[:-3])
                exec("from "+pluginsFolder+"."+elem[:-3]+" import "+elem[:-3])
                #print("system = "+elem[:-3]+"(\""+elem[:-3]+"\", \""+configFile+"\")")
                exec("system = "+elem[:-3]+"(\""+elem[:-3]+"\", \""+configFile+"\")")
                #print("self.root.addChild('plugin', \""+elem[:-3]+"\", system.getTree())")
                exec("self.root.addChild('plugin', \""+elem[:-3]+"\", system.getTree())")
            if os.path.isdir("./"+pluginsFolder+"/"+elem):
                print "path: "+"./"+pluginsFolder+"/"+elem
                self.root.addContainer(elem, "test")

        # LOAD ITUNES PLUGIN MANUALLY

        # create library object, first parameter,
        # Add ITunes Plugin to tree
        # self.root.addChild("iTunes", iTunes("iTunes").getTree())

        # add container test
        #root.addContainer("test", "test information")


    def getTree(self):
        return self.root
    