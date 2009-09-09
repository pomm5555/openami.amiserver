import httplib2
from urllib import urlencode
import os, sys
from AmiTree import Container
from PlugIn import PlugIn



class Prowly(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"

        #plugin itself
        self.content = Container("plugin", token, "this is a Prowl plugin")

        # set add container
        self.content.addContainer("cmd","Prowl", "send Push notification", self.prowl)

    def prowl(self, text="Notification"):
        text = self.getText(text)
        print text

        try:
            f = open(os.getenv("HOME")+"/.prowl")
            username = f.readline().strip()
            password = f.readline().strip()
        except():
            print "create ~/.prowl with your prowl credentials in \\n seperated parts."


        application = "amiServer"
        event = "Notification"
        description = text

        theurl = "https://prowl.weks.net/api/add_notification.php?"

        http = httplib2.Http()
        http.add_credentials(username, password)
        response, content = http.request(theurl + urlencode( {"application":application, "event": event, "description": description}),"GET")

        if response:
            if response.status != 200:
                return "Could not notify"
            else:
                return "Notified"
        else:
            return "Error notificating"


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















