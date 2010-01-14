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
        jid = Config.get("server", "token")


        liElements = []

        #json is the json multi request
        json = ''
        
        #refresher is the code that refreshes the classes
        refresher = ''
        id=0
	for item in config.sections():
            id+=1
            smalltext = config.get(item, 'smalltext')
            largetext = config.get(item, 'largetext')
            icon = config.get(item, 'icon')
            smalltextid = (smalltext+str(id)).replace('/', '_')
            largetextid = (largetext+str(id)).replace('/', '_')

            #codegeneration for largetext
            if largetext.startswith('/'):
                #build the json request
                json += '"'+largetextid+'":"'+largetext+'",'
                #build the refreshing code
                #$(".title").html(playingdata[1]);
                refresher += '$(".'+largetextid+'").html(data["'+largetextid+'"]);\n'

            #codegeneration for smalltext
            if smalltext.startswith('/'):
                #build the json request
                json += '"'+smalltextid+'":"'+smalltext+'",'
                #build the refreshing code
                #$(".title").html(playingdata[1]);
                refresher += '$(".'+smalltextid+'").html(data["'+smalltextid+'"]);\n'

            
            #liElements.append('<div class="dashboardiconcontainer"><img src="'+Config.get("server", "token")+'/'+config.get(item, 'icon')+'" class="dashboardicon"/></div><span class="amiDash1">'+config.get(item, 'largetext')+'</span><em>'+config.get(item, 'smalltext')+'</em>')
            liElements.append('<div class="dashboardiconcontainer"><img src="'+jid+'/'+icon+'" class="dashboardicon"/></div><span class="amiDash1 '+largetextid+'">'+largetext+'</span><em class="'+smalltextid+'">'+smalltext+'</em>')

        json = '{'+json[:-1]+'}'
        print refresher



        javascript = """
<script type="text/javascript">

                $('#dashboard').
                    bind("pageAnimationStart", function(e, info){
                    
                        if (info.direction == 'in'){
                            dashinterval=window.setInterval('update()', 5000);
                        } else {
                            dashinterval=window.clearInterval(dashinterval);
                        }
                    });

function update() {

        function delay(delay) {
            var startTime = new Date();
            var endTime = null;
            do {
                endTime = new Date();
            } while ((endTime - startTime) < delay);
        }

	$.getJSON('"""+jid+"""/Services/multirequest?string="""+json+"""', function(data){

        """+refresher+"""
                    
	});
}

update();

</script>
"""


#<<<<<<< local
#=======
#
#	for item in config.sections():
#            smalltextid = config.get(item, 'smalltext')+config.get(item, 'largetext')+'small'
#            largetextid = config.get(item, 'smalltext')+config.get(item, 'largetext')+'large'
#
#            link = config.get(item,"link")
#
#            if config.get(item,"cam") != "":
#                img = "<img style='-webkit-user-select: none' height="'50'" width="'60'" src="+config.get(item,"cam") + " />"
#            else:
#                img = "<img src="+Config.get("server","token")+"/"+config.get(item,"icon") + " class='dashboardicon'/>"
#
#            liElements.append('<a href="'+link+'"><div class="dashboardcamcontainer">'+img+'</div><span class="amiDash1">'+config.get(item, 'largetext')+'</span><em>'+config.get(item, 'smalltext')+'</em></a>')
#>>>>>>> other


        list = ""
        for elem in liElements:
            
            list += '<li>'+elem+'</li>'
        list = '<ul class="metal">'+list+'</ul>'
        
        result = '<div id="dashboard"><div class="toolbar"><h1>Result</h1><a class="back" href="#">Back</a></div>'+list+'</div>'+javascript
        
        return result