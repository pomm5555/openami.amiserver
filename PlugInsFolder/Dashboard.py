from Address import Address
from EventEngine import EventEngine

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
            icon = config.get(item, 'icon')
            typ = config.get(item,'type')
            iconid = (icon+str(id)).replace('/', '').replace('http:','').replace('.','')
            link = config.get(item,"link")
            useCam = config.get(item,"cam")
            title = config.get(item,"title")

            if typ=='optionselect':
                option_count = int(config.get(item,"options"))
                
                option0 = config.get(item,"option0")
                option1 = config.get(item,"option1")
                cmd = config.get(item,"cmd")
                img = jid+'/'+icon
                
                options=""
                i=0
                for i in range(option_count):
                    option = config.get(item,"option"+str(i))
                    options +=  '<option value="'+option+'">'+option+'</option>'
                    
                info ='<div class="dashboardiconcontainer" id="'+iconid+'"><img  width="100%" height="100%" src="'+img+'"/></div><em >'+title+'</em>'
                select_open = '<select id='+title+' class="dashboardselect" onchange=$.get("'+Config.get("jabber","jid")+cmd+'?string="+this.value);>'
                optgroup_open  = '<optgroup label="'+title+'">'
                body   = '<option value="'+option0+'">'+option0+'</option><option value="'+option1+'">'+option1+'</option>'
                optgroup_close = '</optgroup>'
                select_close='</select>'
                
                html = info + select_open + optgroup_open + options + optgroup_close + select_close
                
                liElements.append(html)
                
            if typ=='togglelist':
                check=""
                root = config.get(item,'root')
                cmd = config.get(item,'cmd')
                arg0 = config.get(item,'arg0')
                arg1 = config.get(item,'arg1')
                
                address = Address.Address(root)
                for addr in EventEngine.root.getByAddress(address.__str__()).getAddressList():
                    if cmd in addr:
                        on = Config.get("jabber","jid")+"/"+addr+"?string="+arg0
                        off = addr+"?string="+arg1
                        current = addr.replace(root,"").replace(cmd,"")
                        check +='<li>'+current+'<span class="toggle"><input type="checkbox" onChange="alert(test)";/></span></li>\n'
                    print "\n ++ ", addr
                
                
                liElements.append('<a href="'+link+'"><em class="non">'+title+'</em>'+check+'</a>')
                
            
            elif typ=='std':
            
                smalltext = config.get(item, 'smalltext')
                largetext = config.get(item, 'largetext')
                smalltextid = (smalltext+str(id)).replace('/', '_')
                largetextid = (largetext+str(id)).replace('/', '_')

            
                if useCam == "True":
                    img = icon
                else:
                    img = jid+'/'+icon


                if icon.startswith('http'):
                    #build the json request
                    #json += '"'+iconid+'":"'+icon+'",'
                    #build the refreshing code
                    #$(".title").html(playingdata[1]);
                    refresher += '$("#'+iconid+'").css("background", "url(http://home.arcor.de/ka010/labcam.jpg)");\n'
                   # refresher += '$(".'+iconid+'").attr({src : "http://home.arcor.de/ka010/labcam.jpg"});\n'
                    #img=""
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
                    refresher += '$(".'+smalltextid+'").fadeTo("slow",0.65);\n'
                    refresher += '$(".'+smalltextid+'").html(data["'+smalltextid+'"]);\n'
                    refresher += '$(".'+smalltextid+'").fadeTo("slow",1);\n'
            
            #liElements.append('<div class="dashboardiconcontainer"><img src="'+Config.get("server", "token")+'/'+config.get(item, 'icon')+'" class="dashboardicon"/></div><span class="amiDash1">'+config.get(item, 'largetext')+'</span><em>'+config.get(item, 'smalltext')+'</em>')
                liElements.append('<a href="'+link+'"><div class="dashboardiconcontainer" id="'+iconid+'"><img  width="100%" height="100%" src="'+img+'"/></div><em class="non">'+title+'</em><span class="'+largetextid+'">'+largetext+'</span><em class="'+smalltextid+'">'+smalltext+'</em></a>')

        json = '{'+json[:-1]+'}'
        print "\n *** Refresher: " ,refresher



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
        list = '<ul class="edgetoedge">'+list+'</ul>'
        
        result = '<div id="dashboard"><div class="toolbar"><h1>Result</h1><a class="back" href="#">Back</a></div>'+list+'</div>'+javascript
        
        return result