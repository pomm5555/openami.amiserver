# To change this template, choose Tools | Templates
# and open the template in the editor.
# growlnotify -m "hallo" -t "hallo"


import os
from AmiTree import Container
from PlugIn import PlugIn
from amiConfig import Config 
from EventEngine import EventEngine
from Address import Address

class PowerSwitch(PlugIn):

	

    def __init__(self, token, configFile):
        PlugIn.__init__(self)
        self.architecture = "all"
        

        #plugin itself
        self.content = PowerSwitchContainer("plugin", token, "PowerSwitch Plugin")
	self.content.addContainer("cmd","test","TEST")
        # hide Plugin from showing up in xml, search, show...
        self.content.visible = True
        
#	tmp = self.content.addContainer("type","Port0", "Port0 (LAB)", self.set(0,1))        
	
	self.content.addContainer('cmd','toggle','toggle',self.toggle)
	
	on = Container("cmd","ON","on")
	off = Container("cmd","OFF","off")

        # set add container
	on.setUse(self.on0)
	off.setUse(self.off0)
	        
	tmp = PowerSwitchContainer("type","Port0","Port0")
	tmp.addChild(on)
	tmp.addChild(off)
        self.content.addChild(tmp)
        
	
	on1 = Container("cmd","ON","on")
	off1 = Container("cmd","OFF","off")
        tmp1 = Container("type","Port1","Port1")
	tmp1.addChild(on1)                                             
        tmp1.addChild(off1) 
	on1.setUse(self.on1)
	off1.setUse(self.off1)
	self.content.addChild(tmp1)

	on2 = Container("cmd","ON","on")
	off2 = Container("cmd","OFF","off")	
	tmp2 = Container("type","Port2","Port2")
	tmp2.addChild(on2)                                             
	tmp2.addChild(off2)
	on2.setUse(self.on2)
	off2.setUse(self.off2) 
	self.content.addChild(tmp2)                                   
	            
	on3 = Container("cmd","ON","on")
	off3 = Container("cmd","OFF","off")            
	tmp3 = Container("type","Port3","Port3")                          
	tmp3.addChild(on3)                                             
	tmp3.addChild(off3)
	on3.setUse(self.on3)
	off3.setUse(self.off3) 
	self.content.addChild(tmp3) 
	                                           	
	allON = Container("cmd","ON","allOn")
	allOff = Container("cmd", "OFF", "allOff")
	tmpAll = Container("type","All","all")
	tmpAll.addChild(allON)
	tmpAll.addChild(allOff)
	allON.setUse(self.allOn)
	allOff.setUse(self.allOff)
	self.content.addChild(tmpAll)

    
    def toggle(self,var):
        
        addr = Address(self.getParent().getAddress()+'/Port'+var+'/ON')
        print '\n *** toggled: ' , var, " addr: " , addr
        EventEngine.root.getByAddress(addr.__str__()).use
        

    def on0(self, text=""):
    	os.system('/workspace/amiServer/PlugInsSupport/./powerswitch.sh 1 on')
    	
    def off0(self, text=""):                                                   
        os.system('/workspace/amiServer/PlugInsSupport/./powerswitch.sh 1 off')
            		
    
    def on1(self, text=""):
    	os.system('/workspace/amiServer/PlugInsSupport/./powerswitch.sh 2  on')
    	
    def off1(self, text=""):
    	os.system('/workspace/amiServer/PlugInsSupport/./powerswitch.sh 2 off')  
    
    def on2(self, text=""):
    	os.system('/workspace/amiServer/PlugInsSupport/./powerswitch.sh 3 on') 
    
    def off2(self, text=""):
    	os.system('/workspace/amiServer/PlugInsSupport/./powerswitch.sh 3 off')
    	
    def on3(self, text=""):
    	os.system('/workspace/amiServer/PlugInsSupport/./powerswitch.sh 4 on')
    
    def off3(self, text=""):
    	os.system('/workspace/amiServer/PlugInsSupport/./powerswitch.sh 4 off')   
    
    def set(self, port="0", state="0"):
  	os.system('/workspace/amiServer/PlugInsSupport/./powerswitch.sh ' + str(port) + ' on')  	
    
    def off(self, text=""):
    	os.system('echo 0 >> /dev/avrBridge0/ports/portC')
    
    def on(self, text=""):
    	os.system('echo 255 >> /dev/avrBridge0/ports/portC')

    def allOn(self,test=""):
    	os.system('/workspace/amiServer/PlugInsSupport/./powerswitch.sh allon')
    		
    def allOff(self,test=""):
    	os.system('/workspace/amiServer/PlugInsSupport/./powerswitch.sh alloff')
    	    	
    # returns the plugin as a tree
    def getTree(self):
        return self.content

    # just a little helper function
    def getText(self, var):
        try:
            var = var.strings["text"]
            return test
        except:
	    var = 0
	            
class PowerSwitchContainer(Container):

    def toJqHtml(self):
    	
    	if self.visible and not self.content == {}:
    		
    		result=""
    		for k,v in self.content.items():
    			result+=v.toJqHtml()
    		
    		address = self.getAddress().replace("/","_").replace("@","_").replace(".","_")
    		token = self.token
		
		on1 = Config.jid+'/PowerSwitch/Port0/ON'
		off1 = Config.jid+'/PowerSwitch/Port0/OFF'    	
    	
                on2 = Config.jid+'/PowerSwitch/Port1/ON'                                      
                off2 = Config.jid+'/PowerSwitch/Port1/OFF' 

                on3 = Config.jid+'/PowerSwitch/Port2/ON'                                      
                off3 = Config.jid+'/PowerSwitch/Port2/OFF' 
                                
                on4 = Config.jid+'/PowerSwitch/Port3/ON'                                      
                off4 = Config.jid+'/PowerSwitch/Port3/OFF' 

		allOn = Config.jid+'/PowerSwitch/All/ON'
		allOff = Config.jid+'/PowerSwitch/All/OFF'
                                    			
    		toolbar = '<div class="toolbar"><h1>'+token+'</h1><a class="back" href="#">Back</a></div>'
    		content_begin = '<ul>'
    		content1 = '<li>Lamp 1<span class="toggle"><input type="checkbox" onChange="if(this.checked) $.get(\''+on1+'\');else $.get(\''+off1+'\');"/></span></li>' 
    		content2 = '<li>Lamp 2<span class="toggle"><input type="checkbox" onChange="if(this.checked) $.get(\''+on2+'\');else $.get(\''+off2+'\');"/></span></li>'
    		content3 = '<li>Lamp 3<span class="toggle"><input type="checkbox" onChange="if(this.checked) $.get(\''+on3+'\');else $.get(\''+off3+'\');"/></span></li>'
    		content4 = '<li>Lamp 4<span class="toggle"><input type="checkbox" onChange="if(this.checked) $.get(\''+on4+'\');else $.get(\''+off4+'\');"/></span></li>'
    		content5 = '<li>All<span class="toggle"><input type="checkbox" onChange="if(this.checked) $.get(\''+allOn+'\');else $.get(\''+allOff+'\');"/></span></li>'
    		content_end = '</ul>'
    		
    		content = content_begin + content1 + content2 + content3 + content4 + content5 + content_end
    		html = "<div id='"+address+"'>"+toolbar+content+"</div>"+result
    		
    		return html
    		
    	else:
		x=0
