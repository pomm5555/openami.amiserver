# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "markus"
__date__ = "$Aug 20, 2009 12:22:08 AM$"
from AmiTree import Container
from amiConfig import Config
import os

class PlugIns:

    def __init__(self, pluginsFolder, configFile):

        #absolute folder to plugins
        absPluginsFolder = os.path.join(Config.absPath, Config.get("Plugins", "PluginPath"))

        #creating list whrer all plugins are loaded in
        self.content = []

        # load all plugins into container
        print "loading all plugins..."
        self.content = self.loadPlugins(absPluginsFolder, pluginsFolder, configFile)

        print "loaded all plugins sucessfully"

        # may not work anymore
        # LOAD ITUNES PLUGIN MANUALLY

        # create library object, first parameter,
        # Add ITunes Plugin to tree
        # self.root.addChild("iTunes", iTunes("iTunes").getTree())

        # add container test
        #root.addContainer("test", "test information")


    def getChildList(self):
        return self.content

    # recursive plugin finder
    def loadPlugins(self, PluginsPath, PackagePath, configFile):


        # get all elements in folder into list
        pluginFiles = os.listdir(PluginsPath)
        #print pluginFiles
        #print PluginsPath, PackagePath

        result = []

        for elem in pluginFiles:
            # add plugin files
            if elem[-3:].__eq__(".py") and not (elem[:1].__eq__("_")):
                print "*** loading: " + PackagePath + "." + elem

                if True: #try:
                    cmd = "from " + PackagePath + "." + elem[:-3] + " import " + elem[:-3]
                    print cmd
                    exec(cmd)
                    print("plugin = "+elem[:-3]+"(\""+elem[:-3]+"\", \""+configFile+"\")")
                    exec("plugin = " + elem[:-3] + "(\"" + elem[:-3] + "\", \"" + configFile + "\")")
                    #print("result.append(plugin.getTree())")
                    #print plugin.architecture


                    # If its a Master Plugin, it only should loaded by Masters, else, check architecture
                    if plugin.master == True:
                        #Check if it amiServer is configured as master
                        if Config.get("server", "master").__eq__("on"):
                            result.append(plugin.getTree())

                    elif plugin.architecture.__eq__("all") or plugin.architecture.__eq__(Config.architecture):
                        result.append(plugin.getTree())

                #except Exception,e:
                #    print "[PLUGIN ERROR] Counld not load Plugin", elem
                #    print e

            # add folders as plugin
            if os.path.isdir(PluginsPath + "/" + elem):
                print "+++ loding folder: " + PluginsPath + "." + elem
                tmpcont = Container("folder", elem, "this is the tree representation of a folder")
                tmpcont.setUse(self.display)
                tmpcont.addChildList(self.loadPlugins(PluginsPath + "/" + elem, PackagePath + "." + elem, configFile))
                result.append(tmpcont)
  
        return result


    def display(self, string=""):
        return self.toHtml()


