import os, urllib2, sys
from AmiTree import *
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

        global user, host, port
        user = Config.get("LastFM", "user")
        host = Config.get("LastFM", "host")
        port = Config.get("LastFM", "port")


        #for pair in Config.getSection("LastFM"):
        #    global user,host,port
        #    if (pair[0] == "user"):
        #        user = pair[1]
        #    if (pair[0] == "host"):
        #        host = pair[1]
        #    if (pair[0] == "port"):
        #        port = pair[1]

        print user,host,port
        love = Container("cmd","Love","love")
        skip = Container("cmd","Skip","skip")
        ban = Container("cmd","Ban","ban")
        stop = Container("cmd","Stop","stop")
        playlist = Container("cmd","Playlist","playlist")
        library = Container("cmd","Library","Library")
        neighbours = Container("cmd","Neighbours","neighbours")
        similar = Container("cmd","Similar","Play similar artist")
        now_playing = Container("cmd","Now Playing","get Now Playing Info")
        coverart = Container("cmd","CoverArt", "get CoverART")
        coverartimage = Container("cmd","CoverArtImage", "get CoverART Image")
        getstate = Container("cmd","State", "get Player State")
        tag = Container("cmd", "Tag", "find Music by Tag")

        love.setUse(self.love)
        skip.setUse(self.skip)
        ban.setUse(self.ban)
        stop.setUse(self.stop)
        playlist.setUse(self.playlist)
        library.setUse(self.library)
        neighbours.setUse(self.neighbours)
        similar.setUse(self.similar)
        now_playing.setUse(self.getNp)
        coverart.setUse(self.getCoverArt)
        coverart.lastCover = ''
        coverart.lastImg = ''
        coverart.rendering = Container.PLAIN
        coverartimage.setUse(self.getCoverArtImage)
        coverartimage.rendering = Container.PLAIN

        getstate.setUse(self.getState)
        tag.setUse(self.tag)
        
        self.content.addChild(love)
        self.content.addChild(ban)
        self.content.addChild(skip)
        self.content.addChild(stop)
        self.content.addChild(playlist)
        self.content.addChild(library)
        self.content.addChild(neighbours)
        self.content.addChild(similar)
        self.content.addChild(now_playing)
        self.content.addChild(coverart)
        self.content.addChild(coverartimage)
        self.content.addChild(getstate)
        self.content.addChild(tag)
        
        # UI Elements
        self.content.addChild(TextfieldContainer("ui", "SimilarArtist", "PlaySimilarArtiest", target=Config.jid+"/Audio/LastFM/Similar"))

    def stop(self,var):
        #print "Stop"
        os.system("echo 'stop' | nc " +host + " " + port)

    def neighbours(self,var):
        #print "LastFm Neighbours"
        os.system("echo 'play lastfm://user/"+user+"/neighbours' | nc " + host + " " + port)
    
    def playlist(self,var):
        #print "LastFm Playlist"
        #print host,port
        os.system("echo 'play lastfm://user/"+user+"/playlist' | nc " +host + " " + port)

    def library(self,var):
        #print "LastFm Library"
        os.system("echo 'play lastfm://user/"+user+"/library' | nc " +host + " " + port)

    def ban(self,var):
        #print "LastFm Ban"
        os.system("echo 'ban' | nc " +host + " " + port)

    def love(self,var):
        #print "LastFm Love"
        os.system("echo 'love' | nc " + host + " " + port)

    def skip(self,var):
        #print "LastFm Skip"
        os.system("echo 'skip' | nc " + host + " " + port)


    def similar(self, artist):
        #print "LastFm similar"
        # lastfm://artist/cher/similarartists
        os.system("echo 'play lastfm://artist/"+artist+"/similarartists' | nc " + host + " " + port)
        
    def tag(self, tag):
        #print "LastFm Tag"
        
        os.system("echo 'play lastfm://tag/"+tag+"' | nc " + host + " " + port)

    def getNp(self,var):
        #print "LastFM  get now Playing"
        #info = pipe = os.popen("curl http://192.168.1.131","r")
        info = os.popen('echo info | nc ' + host + ' ' + port)
        np = info.read().replace('"',"")
	return np
        
    def getCoverArt(self,var):
        np = os.popen('echo info | nc ' + host + ' ' + port)
	#np = pipe = os.popen("curl http://192.168.1.131","r")
        np = np.read()
        print "\n*********", np
        (artist, song, album) = np.split(' - ')
        #print artist, song, album
        np = artist

        if not self.lastCover == artist+song+album:
            self.lastCover = artist+song+album
            import ecs

            ecs.setLicenseKey('AKIAIICBON46BQIRCOUQ')
            ecs.setSecretKey('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')
            #print "** Searching Amazon for "+artist+" "+album
            search = ecs.ItemSearch(Keywords='Music', SearchIndex='Music',Artist=artist, Title=album, ResponseGroup='Images')
            img=search.next().LargeImage.URL
            #print img
            self.lastImg = img
            #print "LastFM getCoverArt!!!!!!!!!!!"

            return img
        else:
            #print 'LOADING CACHED IMAGE FOR COVERART!!!'+self.lastImg
            return self.lastImg

    def getCoverArtImage(self,var):
        addr = Address('/Audio/LastFM/CoverArt')
        imgurl = self.root().getByAddress(addr.__str__()).use()
        #print imgurl
        img = urllib2.urlopen(imgurl).read()
        return img


    def getState(self, var):
        #print "LastFM getState"
        np = os.popen('echo info | nc ' + host + ' ' + port).read()
        if np == ' -  - ':
          return "not playing"
        else:
          return "playing"
          
    # just a little helper function
    def getText(self, var):
        try:
            var = var.strings["text"]
            return test
        except:
            return var
