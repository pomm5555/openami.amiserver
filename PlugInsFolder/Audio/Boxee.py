import os, urllib2, sys
from AmiTree import *
from PlugIn import PlugIn
from amiConfig import Config
import re
class Boxee(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"


        #plugin itself
        self.content = Container("plugin", token, "Boxee Plugin")

        # hide Plugin from showing up in xml, search, show...
        self.content.visible = True

        global user, host, port
        user = Config.get("Boxee", "user")
        host = Config.get("Boxee", "host")
        port = Config.get("Boxee", "port")


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
        pause = Container("cmd","Pause","pause")
        now_playing = Container("cmd","Now Playing","get Now Playing Info")
        coverart = Container("cmd","CoverArt", "get CoverART")
        coverartimage = Container("cmd","CoverArtImage", "get CoverART Image")
        getstate = Container("cmd","State", "get Player State")
        tag = Container("cmd", "Tag", "find Music by Tag")
        similar = Container("cmd","Similar","Play similar artist")
        
        love.setUse(self.love)
        skip.setUse(self.skip)
        ban.setUse(self.ban)
        stop.setUse(self.stop)
        playlist.setUse(self.playlist)
        library.setUse(self.library)
        pause.setUse(self.pause)
        now_playing.setUse(self.getNp)
        similar.setUse(self.similar)
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
        self.content.addChild(pause)
        self.content.addChild(now_playing)
        self.content.addChild(coverart)
        self.content.addChild(coverartimage)
        self.content.addChild(getstate)
        self.content.addChild(tag)
        self.content.addChild(similar)
        
        # UI Elements
        self.content.addChild(TextfieldContainer("ui", "SimilarArtist", "PlaySimilarArtiest", target=Config.jid+"/Audio/LastFM/Similar"))

    def stop(self,var):
        #print "Stop"
        os.system("curl http://" + host + ":"+port+"/xbmcCmds/xbmcHttp?command=Stop")

    def similar(self,artist):
        #print "LastFm Neighbours"
        os.system("curl http://" + host + ":"+port+"/xbmcCmds/xbmcHttp?command=ExecBuiltIn\(PlayMedia\('lastfm://artist/"+artist+"/similarartist'\)\)")

    def neighbours(self,var):
       #print "LastFm Neighbours"
       os.system("curl http://" + host + ":"+port+"/xbmcCmds/xbmcHttp?command=ExecBuiltIn\(PlayMedia\('lastfm://user/ka010/neighbours'\)\)")

    
    def playlist(self,var):
        #print "LastFm Playlist"
        #print host,port
        os.system("curl http://" + host + ":"+port+"/xbmcCmds/xbmcHttp?command=ExecBuiltIn\(PlayMedia\('lastfm://user/ka010/radio'\)\)")

    def library(self,var):
        #print "LastFm Library"
        os.system("curl http://" + host + ":"+port+"/xbmcCmds/xbmcHttp?command=ExecBuiltIn\(PlayMedia\(lastfm://user/ka010/library\)\)")

    def ban(self,var):
        #print "LastFm Ban"
        os.system("curl http://" + host + ":"+port+"/xbmcCmds/xbmcHttp?command=ExecBuiltIn\(LastFM.Ban\(false\)\)")

    def love(self,var):
        #print "LastFm Love"
        os.system("curl http://" + host + ":"+port+"/xbmcCmds/xbmcHttp?command=ExecBuiltIn\(LastFM.Love\(false\)\)")

    def skip(self,var):
        #print "LastFm Skip"
        os.system("curl http://" + host + ":"+port+"/xbmcCmds/xbmcHttp?command=PlayNext")


    def pause(self, var):
        #print "LastFm similar"
        # lastfm://artist/cher/similarartists
        os.system("curl http://" + host + ":"+port+"/xbmcCmds/xbmcHttp?command=Pause")
        
    def tag(self, tag):
        #print "LastFm Tag"
        
        os.system("curl http://" + host + ":"+port+"/xbmcCmds/xbmcHttp?command=ExecBuiltIn\(PlayMedia\(lastfm://tag/test\)\)")

    def getNp(self,var):
        #print "LastFM  get now Playing"
        #info = pipe = os.popen("curl http://192.168.1.131","r")
        info =         os.popen("curl http://" + host + ":"+port+"/xbmcCmds/xbmcHttp?command=GetCurrentlyPlaying")
        np = info.read().replace(":","").splitlines()
        artist = np[6].replace("<li>","").replace("Artist","")
        album = np[7].replace("<li>","").replace("Album","")
        title = np[5].replace("<li>","").replace("Title","")
        np = artist + " - " + title + " - " + album
	return np
        
    def getCoverArt(self,var):
        np = os.popen("curl http://localhost:8080/ami.lab@aminet.org/Audio/Boxee/Now_Playing").read()
	#np = pipe = os.popen("curl http://192.168.1.131","r")
       
        np = re.sub(r'<[^>]*?>', '', np)
        np = np.replace("Back","").replace("Result","")
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
        addr = Address('/Audio/Boxee/CoverArt')
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
