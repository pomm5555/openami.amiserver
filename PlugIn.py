# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="markus"
__date__ ="$Aug 16, 2009 3:48:26 PM$"


#from AmiTree import Container


class PlugIn:

    def __init__(self):
        self.content = None
        self.architecture = "all"
        self.master = False # Use True on your Plugin if you want to use your Plugin only on amiMasters!

    def getTree(self):
        return self.content


