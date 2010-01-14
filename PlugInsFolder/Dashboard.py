from ConfigParser import ConfigParser
from amiConfig import Config
from AmiTree import Container
from PlugIn import PlugIn
import Address

class Dashboard(PlugIn):


    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"

        #plugin itself
        self.content = Container("plugin", token, "This is a Status Plugin", self.getParts)
        self.content.rendering = Container.PLAIN
       	self.content.visible = False

    def getParts(self, text=""):
        string = ""

        #getting stuff from seperate config file
        config = ConfigParser()
        configpath = Config.absPath+'/properties/dashboard.properties'
        config.readfp(open(configpath))

     
        javascript = """
<script type="text/javascript">

                $('#audioplayer').
                    bind("pageAnimationStart", function(e, info){
                        if (info.direction == 'in'){
                            intInterval=window.setInterval('update()', 5000);
                        } else {
                            intInterval=window.clearInterval(intInterval);
                        }
                    });

coverartcache = 'Not initialized'
npcache = 'Not initialized'

function update() {

        function delay(delay) {
            var startTime = new Date();
            var endTime = null;
            do {
                endTime = new Date();
            } while ((endTime - startTime) < delay);
        }

	$.getJSON('_JID_/Services/multirequest?string={"np":"/Defaults/nowplaying","coverart":"/Defaults/coverart", "state":"/Defaults/state"}', function(data){
                playingdata = data["np"].split(' - ')
                //alert(data['coverart']+'/'+coverartcache)


                    $(".title").html(playingdata[1]);
                    $(".interpreter").html(playingdata[0]);
                    $(".coverartbg").css('background', 'url(_JID_/Audio/LastFM/CoverArtImage?'+ts+') no-repeat center center');
	});
}

update();

</script>
"""

        liElements = []

    
	for item in config.sections():
            smalltextid = config.get(item, 'smalltext')+config.get(item, 'largetext')+'small'
            largetextid = config.get(item, 'smalltext')+config.get(item, 'largetext')+'large'
            
            link = config.get(item,"link")
            
            if config.get(item,"cam") != "":
                img = "<img style='-webkit-user-select: none' height="'50'" width="'60'" src="+config.get(item,"cam") + " />"
            else:
                img = "<img src="+Config.get("server","token")+"/"+config.get(item,"icon") + " class='dashboardicon'/>"
            
            liElements.append('<a href="'+link+'"><div class="dashboardcamcontainer">'+img+'</div><span class="amiDash1">'+config.get(item, 'largetext')+'</span><em>'+config.get(item, 'smalltext')+'</em></a>')

        print 'string={"np":"/Defaults/nowplaying","coverart":"/Defaults/coverart", "state":"/Defaults/state"}'

        
        list = ""
        for elem in liElements:
            
            list += '<li>'+elem+'</li>'
        list = '<ul class="metal">'+list+'</ul>'
        
        result = '<div id="dashboard"><div class="toolbar"><h1>Result</h1><a class="back" href="#">Back</a></div>'+list+'</div>'
        
        return result