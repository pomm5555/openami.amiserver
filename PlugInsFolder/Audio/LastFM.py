import os
from AmiTree import Container
from PlugIn import PlugIn
from amiConfig import Config

class LastFM(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"


        #plugin itself
        self.content = Container("plugin", token, "LastFM Plugin")

        # hide Plugin from showing up in xml, search, show...
        self.content.visible = True

        for pair in Config.getSection("LastFM"):
            global user,host,port
            if (pair[0] == "user"):
                user = pair[1]
            if (pair[0] == "host"):
                host = pair[1]
            if (pair[0] == "port"):
                port = pair[1]

        print user,host,port
        love = Container("cmd","Love","love")
        skip = Container("cmd","Skip","skip")
        ban = Container("cmd","Ban","ban")
        quit = Container("cmd","Quit","quit")
        playlist = Container("cmd","Playlist","playlist")
        library = Container("cmd","Library","Library")
        neighbours = Container("cmd","Neighbours","neighbours")

        love.setUse(self.love)
        skip.setUse(self.skip)
        ban.setUse(self.ban)
        quit.setUse(self.quit)
        playlist.setUse(self.playlist)
        library.setUse(self.library)
        neighbours.setUse(self.neighbours)

        self.content.addChild(love)
        self.content.addChild(ban)
        self.content.addChild(skip)
        self.content.addChild(quit)
        self.content.addChild(playlist)
        self.content.addChild(library)
        self.content.addChild(neighbours)

    def quit(self,var):
        os.system("echo 'quit' | nc " +self.host + " " + self.port)

    def neighbours(self,var):
        os.system("echo 'play lastfm://user/"+user+"/neighbours' | nc " + host + " " + port)
    def playlist(self,var):
        print host,port
        os.system("echo 'play lastfm://user/"+user+"/playlist' | nc " +host + " " + port)

    def library(self,var):
        os.system("echo 'play lastfm://user/"+user+"/library' | nc " +host + " " + port)

    def ban(self,var):
        os.system("echo 'ban' | nc " +host + " " + port)

    def love(self,var):
        os.system("echo 'love' | nc " + host + " " + port)

    def skip(self,var):
        os.system("echo 'skip' | nc " + host + " " + port)


    # just a little helper function
    def getText(self, var):
        try:
            var = var.strings["text"]
            return test
        except:
            return var